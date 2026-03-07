"""
Legado JavaScript Engine - 完整移植Legado的JS运行环境
使用 Node.js 模拟 Rhino 引擎的执行环境
"""

import os
import json
import re
import subprocess
import tempfile
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class JsExecutionResult:
    success: bool
    result: Any = None
    error: Optional[str] = None
    console_output: List[str] = field(default_factory=list)
    duration_ms: float = 0
    variables: Dict[str, str] = field(default_factory=dict)


LEGADO_JS_FUNCTIONS = '''
var java = {
    base64Decode: function(str, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, 'base64').toString(charset);
            }
            return atob(str);
        } catch (e) {
            return '';
        }
    },
    base64Encode: function(str, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, charset).toString('base64');
            }
            return btoa(str);
        } catch (e) {
            return '';
        }
    },
    encodeURI: function(str, enc) {
        enc = enc || 'UTF-8';
        try {
            return encodeURIComponent(str);
        } catch (e) {
            return str;
        }
    },
    decodeURI: function(str, enc) {
        enc = enc || 'UTF-8';
        try {
            return decodeURIComponent(str);
        } catch (e) {
            return str;
        }
    },
    timeFormatUTC: function(time, format, sh) {
        sh = sh || 0;
        var date = new Date(time);
        var offset = date.getTimezoneOffset() * 60000;
        var utc = new Date(date.getTime() + offset + sh * 3600000);
        var pad = function(n) { return n < 10 ? '0' + n : n; };
        return format
            .replace(/yyyy/g, utc.getFullYear())
            .replace(/yy/g, String(utc.getFullYear()).slice(-2))
            .replace(/MM/g, pad(utc.getMonth() + 1))
            .replace(/M/g, utc.getMonth() + 1)
            .replace(/dd/g, pad(utc.getDate()))
            .replace(/d/g, utc.getDate())
            .replace(/HH/g, pad(utc.getHours()))
            .replace(/H/g, utc.getHours())
            .replace(/mm/g, pad(utc.getMinutes()))
            .replace(/m/g, utc.getMinutes())
            .replace(/ss/g, pad(utc.getSeconds()))
            .replace(/s/g, utc.getSeconds());
    },
    timeFormat: function(time) {
        var date = new Date(time);
        var pad = function(n) { return n < 10 ? '0' + n : n; };
        return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate()) + ' ' +
               pad(date.getHours()) + ':' + pad(date.getMinutes()) + ':' + pad(date.getSeconds());
    },
    log: function(msg) {
        console.log('[Legado] ' + msg);
        return msg;
    },
    toast: function(msg) {
        console.log('[Toast] ' + msg);
        return msg;
    },
    put: function(key, value) {
        if (typeof _variables !== 'undefined') {
            _variables[key] = String(value);
        }
        return value;
    },
    get: function(key) {
        if (typeof _variables !== 'undefined' && _variables[key]) {
            return _variables[key];
        }
        return '';
    },
    randomUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },
    jsonParse: function(str) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return null;
        }
    }
};

var result = '';
var baseUrl = '';
var src = '';
var body = '';
var source = null;
var book = null;
var chapter = null;
var title = '';
var page = 1;
var key = '';
var _variables = {};

function getVariable(key) {
    return java.get(key);
}
function setVariable(key, value) {
    return java.put(key, value);
}
'''


def build_js_lib_wrapper(js_lib_code: str) -> str:
    # 在 Python 端直接替换 this 为 globalThis
    # 只替换 IIFE 调用中的 this，不影响函数参数中的 this
    # IIFE 模式: })(this, 或 })(this) 或 })(this);
    processed_code = js_lib_code
    # 只替换 IIFE 结尾的 this
    # 模式: })(this, 或 })(this) 或 })(this);
    processed_code = processed_code.replace('})(this,', '})(globalThis,')
    processed_code = processed_code.replace('})(this)', '})(globalThis)')
    processed_code = processed_code.replace('})(this);', '})(globalThis);')
    
    # 替换 CommonJS 检测条件，强制走全局变量分支
    # 将 typeof exports === "object" 替换为 false
    processed_code = processed_code.replace('typeof exports === "object"', 'false')
    processed_code = processed_code.replace('typeof exports==="object"', 'false')
    processed_code = processed_code.replace('typeof define === "function" && define.amd', 'false')
    processed_code = processed_code.replace('typeof define==="function"&&define.amd', 'false')
    
    js_lib_json = json.dumps(processed_code)
    return '''
(function() {
    try {
        // 使用间接 eval (0, eval) 在全局作用域执行代码
        // 这样函数声明会创建全局变量
        (0, eval)(''' + js_lib_json + ''');
    } catch (e) {
        console.log('[JS Engine] Error executing jsLib:', e.message);
        console.log('[JS Engine] Stack:', e.stack);
    }
})();

(function() {
    var detectedVars = [];
    var knownBuiltins = ['java', 'result', 'baseUrl', 'src', 'body', 'source', 'book', 'chapter', 'title', 'page', 'key', '_variables', 'console', 'global', 'globalThis', 'process', 'Buffer', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'module', 'exports', 'require', '__filename', '__dirname', 'clearImmediate', 'setImmediate', 'queueMicrotask', 'structuredClone', 'atob', 'btoa', 'performance', 'fetch', 'crypto', 'navigator', 'localStorage', 'sessionStorage'];
    
    for (var key in globalThis) {
        if (knownBuiltins.indexOf(key) === -1) {
            var val = globalThis[key];
            if (typeof val === 'function') {
                detectedVars.push(key + '()');
            } else if (typeof val === 'object' && val !== null) {
                detectedVars.push(key + ' {}');
            } else {
                detectedVars.push(key);
            }
        }
    }
    
    if (detectedVars.length > 0) {
        console.log('[JS Engine] Detected global variables from jsLib: ' + detectedVars.join(', '));
    } else {
        console.log('[JS Engine] WARNING: No global variables detected from jsLib');
    }
})();
'''


class LegadoJsEngine:
    def __init__(self):
        self.node_path = self._find_node()
        self.engine_type = 'node' if self.node_path else 'python'
    
    def _find_node(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'node'
        except:
            pass
        return None
    
    def execute(
        self,
        js_code: str,
        context: Dict[str, Any] = None,
        js_lib: str = None,
        timeout: int = 30
    ) -> JsExecutionResult:
        start_time = time.time()
        context = context or {}
        
        context_js = "// Context variables\n"
        for key, value in context.items():
            if isinstance(value, str):
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                context_js += f'var {key} = "{escaped_value}";\n'
            elif isinstance(value, (int, float, bool)):
                context_js += f'var {key} = {json.dumps(value)};\n'
            elif isinstance(value, (dict, list)):
                context_js += f'var {key} = {json.dumps(value, ensure_ascii=False)};\n'
            elif value is None:
                context_js += f'var {key} = null;\n'
        
        js_lib_code = js_lib or ''
        js_lib_wrapper = build_js_lib_wrapper(js_lib_code)
        
        full_code = f'''
{LEGADO_JS_FUNCTIONS}

// ==================== Context ====================
{context_js}

// ==================== jsLib ====================
{js_lib_wrapper}

// ==================== User Code ====================
{js_code}

// ==================== Output ====================
if (typeof body !== 'undefined' && body) {{
    result = body;
}}

console.log('<<<RESULT_START>>>');
try {{
    console.log(JSON.stringify({{result: result}}));
}} catch (e) {{
    console.log(JSON.stringify({{result: String(result)}}));
}}
console.log('<<<RESULT_END>>>');
'''
        
        if self.engine_type == 'node':
            exec_result = self._execute_with_node(full_code, timeout)
        else:
            exec_result = self._execute_with_python(full_code, timeout)
        
        exec_result.duration_ms = (time.time() - start_time) * 1000
        return exec_result
    
    def _execute_with_node(self, code: str, timeout: int) -> JsExecutionResult:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            result = subprocess.run(
                ['node', temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            try:
                os.unlink(temp_path)
            except:
                pass
            
            output = result.stdout
            console_output = []
            js_result = None
            
            if '<<<RESULT_START>>>' in output:
                parts = output.split('<<<RESULT_START>>>')
                console_output = parts[0].strip().split('\n') if parts[0].strip() else []
                result_part = parts[1].split('<<<RESULT_END>>>')[0].strip()
                try:
                    parsed = json.loads(result_part)
                    js_result = parsed.get('result')
                except:
                    js_result = result_part
            else:
                console_output = output.strip().split('\n') if output.strip() else []
            
            if result.returncode != 0:
                return JsExecutionResult(
                    success=False,
                    result=None,
                    error=result.stderr or 'Unknown error',
                    console_output=console_output
                )
            
            return JsExecutionResult(
                success=True,
                result=js_result,
                console_output=console_output
            )
            
        except subprocess.TimeoutExpired:
            return JsExecutionResult(success=False, error=f"Timeout ({timeout}s)")
        except Exception as e:
            return JsExecutionResult(success=False, error=str(e))
    
    def _execute_with_python(self, code: str, timeout: int) -> JsExecutionResult:
        try:
            import js2py
            result = js2py.eval_js(code)
            return JsExecutionResult(success=True, result=result)
        except ImportError:
            return JsExecutionResult(success=False, error="Please install Node.js")
        except Exception as e:
            return JsExecutionResult(success=False, error=str(e))
    
    def execute_rule(
        self,
        rule: str,
        content: str,
        base_url: str = "",
        js_lib: str = None,
        variables: Dict[str, str] = None
    ) -> JsExecutionResult:
        if '@js:' in rule:
            js_code = rule.split('@js:')[1].strip()
        elif rule.startswith('<js>'):
            match = re.search(r'<js>(.*?)</js>', rule, re.DOTALL)
            js_code = match.group(1).strip() if match else rule[4:].strip()
        else:
            return JsExecutionResult(success=False, error="Not a JS rule")
        
        context = {
            'result': content,
            'src': content,
            'body': content,
            'baseUrl': base_url,
            '_variables': variables or {},
        }
        
        return self.execute(js_code, context, js_lib)


class JsExtensions:
    @staticmethod
    def base64_decode(str_val: str, charset: str = 'utf-8') -> str:
        try:
            return base64.b64decode(str_val).decode(charset)
        except:
            return ""
    
    @staticmethod
    def base64_encode(str_val: str, charset: str = 'utf-8') -> str:
        try:
            return base64.b64encode(str_val.encode(charset)).decode('utf-8')
        except:
            return ""
    
    @staticmethod
    def time_format(time_ms: int) -> str:
        try:
            from datetime import datetime
            return datetime.fromtimestamp(time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ""
    
    @staticmethod
    def encode_uri(str_val: str, enc: str = 'UTF-8') -> str:
        from urllib.parse import quote
        try:
            return quote(str_val, safe='')
        except:
            return ""
    
    @staticmethod
    def decode_uri(str_val: str, enc: str = 'UTF-8') -> str:
        from urllib.parse import unquote
        try:
            return unquote(str_val)
        except:
            return ""
    
    @staticmethod
    def md5_encode(str_val: str) -> str:
        import hashlib
        return hashlib.md5(str_val.encode('utf-8')).hexdigest()


_js_engine: Optional[LegadoJsEngine] = None


def get_js_engine() -> LegadoJsEngine:
    global _js_engine
    if _js_engine is None:
        _js_engine = LegadoJsEngine()
    return _js_engine


def execute_js(js_code: str, context: Dict[str, Any] = None, js_lib: str = None) -> JsExecutionResult:
    return get_js_engine().execute(js_code, context, js_lib)


def execute_js_rule(rule: str, content: str, base_url: str = "", js_lib: str = None, variables: Dict[str, str] = None) -> JsExecutionResult:
    return get_js_engine().execute_rule(rule, content, base_url, js_lib, variables)
