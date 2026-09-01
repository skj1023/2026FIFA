const fs = require('fs');
const html = fs.readFileSync('index.html','utf8');
const m = html.match(/const ALL_MATCHES = \[([\s\S]*?)\];/);
if(!m){console.log('NO ALL_MATCHES FOUND');process.exit(1);}
const arr = eval('['+m[1]+']');
let done=0,live=0,up=0;
arr.forEach(x=>{if(x.st==='done')done++;else if(x.st==='live')live++;else up++;});
console.log('Total:',arr.length,'Done:',done,'Live:',live,'Upcoming:',up);
// Check final
const fin = arr.find(x=>x.id==='FIN');
console.log('FIN:', JSON.stringify({id:fin.id,s:fin.s,st:fin.st,h:fin.h,a:fin.a}));
const third = arr.find(x=>x.id==='3RD');
console.log('3RD:', JSON.stringify({id:third.id,s:third.s,st:third.st,h:third.h,a:third.a}));
// Check all KO matches have st=done
const koMatches = arr.filter(x=>x.g==='KO');
console.log('KO matches:', koMatches.length);
const koNotDone = koMatches.filter(x=>x.st!=='done');
console.log('KO not done:', koNotDone.length, koNotDone.map(x=>x.id));
// Check group matches
const groupMatches = arr.filter(x=>x.g!=='KO');
console.log('Group matches:', groupMatches.length);
const groupNotDone = groupMatches.filter(x=>x.st!=='done');
console.log('Group not done:', groupNotDone.length);
// Check hero text
const heroChampion = html.includes('西班牙') && html.includes('冠军');
console.log('Hero has champion Spain:', heroChampion);
// Check info tab for post-tournament message
const infoEnd = html.includes('本届世界杯已结束');
console.log('Info tab has ended message:', infoEnd);
// Check SCORERS
const scorersM = html.match(/const SCORERS\s*=\s*\[([\s\S]*?)\];/);
if(scorersM) {
  const scorers = eval('['+scorersM[1]+']');
  console.log('SCORERS count:', scorers.length);
  scorers.slice(0,5).forEach(s => console.log('  ', JSON.stringify(s)));
} else {
  console.log('No SCORERS found');
}
