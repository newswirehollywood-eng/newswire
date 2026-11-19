// node tools/cards/make_card.js <brand> "<kicker>" "<title>" <out.jpg>
// Optional 5th argument: a licensed photo to put behind the headline.
// Run with: NODE_PATH=$(npm root -g) node tools/cards/make_card.js ...
const {chromium}=require('playwright');const path=require('path');
const [brand,kicker,title,out,photo]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
const o={brand,kicker,title};if(photo)o.photo='file://'+path.resolve(photo);const q=new URLSearchParams(o).toString();
await p.goto('file://'+path.join(__dirname,'card.html')+'?'+q);await p.waitForTimeout(2000);
await p.screenshot({path:out,type:'jpeg',quality:90,clip:{x:0,y:0,width:1080,height:1080}});await b.close();console.log(out);})();
