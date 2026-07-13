const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('index.html','utf8');
function extract(name){
  const re = new RegExp(`const ${name}\\s*=\\s*([\\s\\S]*?\\n\\]);`);
  const m = html.match(re);
  if(!m) throw new Error('not found: '+name);
  return m[1];
}
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext('ALL_MATCHES = ' + extract('ALL_MATCHES'), sandbox);
const arr = sandbox.ALL_MATCHES;
const counts = {};
for(const x of arr) counts[x.st] = (counts[x.st]||0)+1;
console.log(JSON.stringify({total:arr.length, counts, lastDone:arr.filter(x=>x.st==='done').slice(-10), upcoming:arr.filter(x=>x.st!=='done').slice(0,12)}, null, 2));
