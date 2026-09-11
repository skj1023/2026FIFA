const fs=require('fs');
const html=fs.readFileSync('C:/Users/PC/Documents/2026FIFA/index.html','utf8');
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
console.log('scriptCount='+scripts.length);
let failed=0;
scripts.forEach((code,i)=>{
  const path=`C:/Users/PC/Documents/2026FIFA/_cron_syntax_20260912_0624_${i}.js`;
  fs.writeFileSync(path, code, 'utf8');
});
