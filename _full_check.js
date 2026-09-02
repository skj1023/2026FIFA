const fs=require('fs');
const html=fs.readFileSync('index.html','utf-8');

// Extract all script blocks
const scripts=[];
let re=/<script[^>]*>([\s\S]*?)<\/script>/g;
let m;
while((m=re.exec(html))!==null){
  if(m[1].trim().length>100) scripts.push(m[1]);
}

console.log('=== Script blocks found:',scripts.length);

// Extract ALL_MATCHES
const amMatch=html.match(/const ALL_MATCHES\s*=\s*(\[[\s\S]*?\]);/);
if(!amMatch){console.log('ERROR: ALL_MATCHES not found');process.exit(1);}

// Use Function constructor to evaluate
const arr=(new Function('return '+amMatch[1]))();
const done=arr.filter(x=>x.st==='done');
const upcoming=arr.filter(x=>x.st==='upcoming');
const live=arr.filter(x=>x.st==='live');

console.log('=== ALL_MATCHES Summary ===');
console.log('Total matches:',arr.length);
console.log('Done:',done.length);
console.log('Upcoming:',upcoming.length);
console.log('Live:',live.length);

// Check final match
const fin=arr.find(x=>x.id==='FIN');
if(fin) console.log('Final:',fin.h,'vs',fin.a,'score:',fin.sc,'st:',fin.st);

// Check 3rd place
const third=arr.find(x=>x.id==='3RD');
if(third) console.log('3rd:',third.h,'vs',third.a,'score:',third.sc,'st:',third.st);

// Check KO matches
const ko=arr.filter(x=>x.g==='KO');
console.log('KO matches:',ko.length);
const koUpcoming=ko.filter(x=>x.st==='upcoming');
const koLive=ko.filter(x=>x.st==='live');
const koDone=ko.filter(x=>x.st==='done');
console.log('  done:',koDone.length,'upcoming:',koUpcoming.length,'live:',koLive.length);

// Group stage
const gs=arr.filter(x=>x.g!=='KO');
const gsDone=gs.filter(x=>x.st==='done');
console.log('Group stage:',gs.length,'done:',gsDone.length);

// Check for TBD in KO matches
const tbdMatches=arr.filter(x=>x.g==='KO'&&(x.h.includes('待定')||x.a.includes('待定')));
console.log('KO matches with TBD:',tbdMatches.length);
if(tbdMatches.length>0){
  tbdMatches.forEach(x=>console.log('  WARNING:',x.id,x.h,'vs',x.a));
}

// Check SCORERS
const scorersMatch=html.match(/const SCORERS\s*=\s*(\{[\s\S]*?\});/);
if(scorersMatch){
  const scorers=(new Function('return '+scorersMatch[1]))();
  const keys=Object.keys(scorers);
  console.log('\n=== SCORERS ===');
  console.log('Count:',keys.length);
  const sorted=keys.map(k=>({name:k,val:scorers[k]})).sort((a,b)=>parseInt(b.val.split(' ')[0])-parseInt(a.val.split(' ')[0]));
  console.log('Top 5:');
  sorted.slice(0,5).forEach(s=>console.log('  '+s.name+': '+s.val));
}

// Check for "赛事未开始" or similar misleading text
const misleading=['即将开始','即将开幕','赛事未开始','敬请期待','待定','暂未','未开赛','小组赛未结束'];
console.log('\n=== Misleading text check ===');
misleading.forEach(term=>{
  const count=(html.match(new RegExp(term,'g'))||[]).length;
  if(count>0) console.log('  WARNING: "'+term+'" found '+count+' times');
  else console.log('  OK: "'+term+'" not found');
});

// Check log entries
const logItems=(html.match(/class="log-item"/g)||[]).length;
console.log('\n=== Log entries:',logItems);

// Check latest log entry marker
const markerMatch=html.match(/marker:cron-post-tournament-check-(\d{8}-\d{4})/);
if(markerMatch) console.log('Latest marker:',markerMatch[1]);

// Check info tab for post-tournament messaging
const hasEnded=html.includes('本届世界杯已结束');
console.log('Info "本届世界杯已结束":',hasEnded);
const hasChampion=html.includes('西班牙夺冠');
console.log('Info "西班牙夺冠":',hasChampion);

// Check allGroupsComplete
const allGSComplete=html.includes('allGroupsComplete');
console.log('allGroupsComplete flag:',allGSComplete);

// Check playedCount
const playedCountMatch=html.match(/id="playedCount"[^>]*>(\d+)/);
if(playedCountMatch) console.log('playedCount display:',playedCountMatch[1]);

// Check final countdown
const fcTitle=html.match(/fc-title">([^<]+)</);
if(fcTitle) console.log('Final countdown title:',fcTitle[1]);

// Check scorers section header
const scorerHeader=html.match(/赛事已全部结束.*最终射手榜|最终射手榜|射手榜.*持续更新/g);
console.log('Scorer headers:',scorerHeader);

console.log('\n=== Validation Complete ===');
if(done.length===104 && upcoming.length===0 && live.length===0 && tbdMatches.length===0){
  console.log('RESULT: ALL CHECKS PASSED - Tournament fully complete, no issues');
}else{
  console.log('RESULT: ISSUES FOUND - Review above');
}
