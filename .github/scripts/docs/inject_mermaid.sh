#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash scripts/docs/inject_mermaid.sh <INDEX_HTML> [MERMAID_VERSION]
# or with env vars INDEX and MERMAID_VERSION

INDEX="${1:-${INDEX:-}}"
MERMAID_VERSION="${2:-${MERMAID_VERSION:-10}}"

if [[ -z "${INDEX}" ]]; then
  echo "INDEX path not provided" >&2
  exit 1
fi

if [[ ! -f "${INDEX}" ]]; then
  echo "Index not found: ${INDEX}"
  exit 0
fi

export INDEX MERMAID_VERSION
python3 - << 'PY'
import os, io

p = os.environ['INDEX']
version = os.environ.get('MERMAID_VERSION', '10')

with io.open(p, 'r', encoding='utf-8', errors='ignore') as f:
    s = f.read()

if '<!-- MERMAID_INJECT_START -->' in s:
    print('Mermaid already injected; skipping.')
else:
    inject = '''\
<!-- MERMAID_INJECT_START -->
<style>.mermaid{max-width:100%;overflow-x:auto}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@__VER__/dist/mermaid.min.js"></script>
<script>
(function(){
  function convertBlocks(root){
    var blocks = root.querySelectorAll('pre code.language-mermaid, pre code.lang-mermaid, code.mermaid');
    blocks.forEach(function(code){
      var txt = code.textContent;
      var pre = code.closest && code.closest('pre') || code;
      var div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = txt;
      if (pre && pre.parentNode) pre.parentNode.replaceChild(div, pre); else code.parentNode.replaceChild(div, code);
    });
  }
  function renderAll(){
    try {
      if (window.mermaid) {
        mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });
        if (mermaid.run) { mermaid.run({ querySelector: '.mermaid' }); }
        else if (mermaid.init) { mermaid.init(undefined, '.mermaid'); }
      }
    } catch(e){ console.error('Mermaid init error', e); }
  }
  function process(){ convertBlocks(document); renderAll(); }
  window.addEventListener('load', function(){
    process();
    var obs = new MutationObserver(function(){
      if (document.querySelector('pre code.language-mermaid, pre code.lang-mermaid, code.mermaid')) {
        process();
      }
    });
    obs.observe(document.body, { childList: true, subtree: true });
  });
})();
</script>
<!-- MERMAID_INJECT_END -->'''
    inject = inject.replace('__VER__', version)

    if '</body>' in s:
        s = s.replace('</body>', inject + '\n</body>', 1)
    else:
        s = s + inject

    with io.open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    print('Injected Mermaid support into', p)
PY

