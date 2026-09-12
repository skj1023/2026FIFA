const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('index.html','utf8');
let scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
if (!scripts.length) throw new Error('no script blocks');
let script = scripts.at(-1)[1];
script = script
  .replace('const TEAMS =', 'globalThis.TEAMS =')
  .replace('const GROUPS =', 'globalThis.GROUPS =')
  .replace('const GROUP_META =', 'globalThis.GROUP_META =')
  .replace('const THIRD_RANK =', 'globalThis.THIRD_RANK =')
  .replace('const SCORERS=', 'globalThis.SCORERS =')
  .replace('const ALL_MATCHES =', 'globalThis.ALL_MATCHES =');
function elem(){ return {innerHTML:'',textContent:'',className:'',value:'',checked:false,style:{},dataset:{},appendChild(){},prepend(){},remove(){},addEventListener(){},setAttribute(){},getAttribute(){return null},querySelector(){return elem()},querySelectorAll(){return []},classList:{add(){},remove(){},toggle(){},contains(){return false}}}; }
const sandbox = {
  console,
  localStorage:{getItem(){return null},setItem(){}},
  window:{addEventListener(){}, matchMedia(){return {matches:false,addEventListener(){}}}, scrollTo(){}},
  document:{
    documentElement:{setAttribute(){},classList:{add(){},remove(){},toggle(){}}},
    body:elem(),
    addEventListener(){}, querySelector(){return elem()}, querySelectorAll(){return []}, getElementById(){return elem()}, createElement(){return elem()}
  },
  setInterval(){}, clearInterval(){}, setTimeout(){}, requestAnimationFrame(fn){ if (typeof fn==='function') fn(); }, location:{protocol:'file:'}, Date
};
sandbox.window.document = sandbox.document;
vm.createContext(sandbox);
vm.runInContext(script, sandbox);
const m=sandbox.ALL_MATCHES, scorers=sandbox.SCORERS;
const byGroup={}; for (const x of m) byGroup[x.g]=(byGroup[x.g]||0)+1;
const ids=m.map(x=>x.id); const dup=ids.filter((id,i)=>ids.indexOf(id)!==i);
const done=m.filter(x=>x.st==='done').length, live=m.filter(x=>x.st==='live').length, upcoming=m.filter(x=>x.st!=='done'&&x.st!=='live').length;
const ko=m.filter(x=>x.g==='KO');
const koPredDraw=ko.filter(x=>x.pred && x.pred.winner==='d').map(x=>x.id);
const tbd=ko.filter(x=>[x.h,x.a,x.s,x.hl].some(v=>String(v||'').includes('TBD'))).map(x=>x.id);
const scorerEntries=Object.entries(scorers).map(([n,v])=>{const p=String(v).split(' '); return {n, team:p[0], g:Number(p[1])};}).sort((a,b)=>b.g-a.g);
const top=scorerEntries.slice(0,6).map(x=>`${x.n}:${x.g}`).join(', ');
const logFirst=(html.match(/<div class="log-time">([^<]+)/)||[])[1];
const bodyHasEnded=html.includes('本届世界杯已结束');
const champion=html.includes('冠军西班牙') || html.includes('西班牙夺冠') || html.includes('世界冠军：西班牙');
const progress=html.includes('104/104') || html.includes('104 场');
const result={matches:m.length,done,live,upcoming,unique:new Set(ids).size,dup,byGroup,ko:ko.length,koPredDraw,tbd,scorers:Object.keys(scorers).length,top,logFirst,marker0945:(html.match(/marker:cron-full-check-20260912-0945/g)||[]).length,bodyHasEnded,champion,progress};
console.log(JSON.stringify(result, null, 2));
if(m.length!==104||done!==104||live||upcoming||new Set(ids).size!==104||dup.length||ko.length!==32||koPredDraw.length||tbd.length||Object.keys(scorers).length!==44||logFirst!=='2026-09-12 09:45'||!bodyHasEnded||!progress||result.marker0945!==1) process.exit(1);
