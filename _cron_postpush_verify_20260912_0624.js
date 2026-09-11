const crypto=require('crypto');
const https=require('https');
const {execFileSync}=require('child_process');
function get(url,timeout=90000){return new Promise((resolve,reject)=>{const req=https.get(url,{headers:{'User-Agent':'Fufu FIFA cron','Cache-Control':'no-cache','Pragma':'no-cache'}},res=>{const bufs=[];res.on('data',d=>bufs.push(d));res.on('end',()=>resolve({status:res.statusCode,data:Buffer.concat(bufs),headers:res.headers}));});req.on('error',reject);req.setTimeout(timeout,()=>req.destroy(new Error('timeout '+url)));});}
(async()=>{
  const fs=require('fs');
  const local=fs.readFileSync('index.html');
  const localSha=crypto.createHash('sha256').update(local).digest('hex');
  const head=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
  const remoteLine=execFileSync('git',['ls-remote','origin','refs/heads/main'],{encoding:'utf8'}).trim();
  console.log('HEAD', head);
  console.log('REMOTE', remoteLine);
  console.log('LOCAL_SHA', localSha);
  for (const [name,url] of [['raw','https://raw.githubusercontent.com/skj1023/2026FIFA/main/index.html?cb=202609120624'],['live','https://fifa.skj1023.top/?v=202609120624']]) {
    const r=await get(url);
    const text=r.data.toString('utf8');
    const sha=crypto.createHash('sha256').update(r.data).digest('hex');
    console.log(name, 'status='+r.status, 'bytes='+r.data.length, 'sha256='+sha, 'marker0624='+(text.match(/marker:cron-full-check-20260912-0624/g)||[]).length, 'marker0415='+(text.match(/marker:cron-full-check-20260912-0415/g)||[]).length, 'firstLog='+(text.match(/<div class="log-time">([^<]+)/)||[])[1]);
  }
})().catch(e=>{console.error(e); process.exit(1);});
