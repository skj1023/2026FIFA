const fs=require('fs');
const html=fs.readFileSync('index.html','utf-8');
const m=html.match(/<script[^>]*>([\s\S]*?)<\/script>/);
if(m){fs.writeFileSync('_temp_syntax.js',m[1]);console.log('OK',m[1].length)}else{console.log('NO_SCRIPT');process.exit(1)}
