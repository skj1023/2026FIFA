const fs=require('fs');
const {JSDOM, VirtualConsole}=require('jsdom');
const html=fs.readFileSync('C:/Users/PC/Documents/2026FIFA/index.html','utf8');
const errors=[];
const vc=new VirtualConsole();
vc.on('jsdomError',e=>errors.push(String(e.message||e)));
vc.on('error',e=>errors.push(String(e)));
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',url:'https://fifa.skj1023.top/',virtualConsole:vc,beforeParse(window){window.scrollTo=()=>{};window.requestAnimationFrame=(cb)=>setTimeout(cb,0);window.fetch=async()=>({ok:false,status:404,text:async()=>'',json:async()=>({})});}});
function wait(ms){return new Promise(r=>setTimeout(r,ms));}
(async()=>{
  await wait(1000);
  const w=dom.window;
  const matches=w.ALL_MATCHES || w.eval('ALL_MATCHES');
  const scorers=w.SCORERS || w.eval('SCORERS');
  const ids=new Set(matches.map(m=>m.id));
  const byGroup={};
  for(const m of matches) byGroup[m.g]=(byGroup[m.g]||0)+1;
  const done=matches.filter(m=>m.st==='done').length;
  const live=matches.filter(m=>m.st==='live').length;
  const upcoming=matches.length-done-live;
  const koDrawPred=matches.filter(m=>m.g==='KO' && m.pred && m.pred.winner==='d').map(m=>m.id);
  const bodyText=w.document.body.textContent;
  const out={
    errors,
    matchCount:matches.length,
    uniqueIds:ids.size,
    done,live,upcoming,
    groupCounts:byGroup,
    scorerCount:Object.keys(scorers).length,
    topScorers:Object.entries(scorers).slice(0,7),
    koDrawPred,
    domMatchCards:w.document.querySelectorAll('.match-card').length,
    playedCount:w.document.getElementById('playedCount')?.textContent,
    matchCountText:w.document.getElementById('matchCount')?.textContent,
    progressPct:w.document.getElementById('progressPct')?.textContent,
    bodyHasEnded:bodyText.includes('本届世界杯已结束'),
    championSpain:bodyText.includes('冠军') && bodyText.includes('西班牙'),
    bracketTBD:Array.from(w.document.querySelectorAll('#tab-bracket .bc-node,#tab-bracket .ko-match')).filter(el=>/TBD/.test(el.textContent)).length,
    logFirst:w.document.querySelector('#updateLogList .log-time')?.textContent.trim().replace(/\s+/g,' '),
    marker0730:(html.match(/marker:cron-full-check-20260912-0730/g)||[]).length,
    marker0624:(html.match(/marker:cron-full-check-20260912-0624/g)||[]).length
  };
  console.log(JSON.stringify(out,null,2));
  dom.window.close();
  const okGroups = 'ABCDEFGHIJKL'.split('').every(g=>byGroup[g]===6) && byGroup.KO===32;
  if(errors.length||out.matchCount!==104||out.uniqueIds!==104||out.done!==104||out.live!==0||out.upcoming!==0||!okGroups||out.koDrawPred.length||out.marker0730!==1||out.marker0624!==1||out.logFirst!=='2026-09-12 07:30'||!out.bodyHasEnded||!out.championSpain||out.bracketTBD!==0) process.exit(1);
  process.exit(0);
})();
