"use strict";
// Original static report presentation. No network, account or storage access.
const reportData = JSON.parse(document.getElementById("report-data").textContent);
const Q = reportData.queries;
const collections = ["Studio V1", "Studio V2", "NVIDIA", "Official humans"];
const colors = {"Studio V1":"#ef64b4","Studio V2":"#ffdc00","NVIDIA":"#67b6ff","Official humans":"#c9c9c9"};
const modes = ["Directions", "Action button", "Click", "Undo"];
const modeColors = {"Directions":"#67b6ff","Action button":"#ef64b4","Click":"#ffdc00","Undo":"#999999"};
const sourceNames = {studio:"Studio V1",studio_v2:"Studio V2",nvidia:"NVIDIA"};
const chartRows = new Map();
const escapeText = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt = value => typeof value === "number" ? Number.isInteger(value) ? value.toLocaleString("en-US") : value.toLocaleString("en-US",{maximumFractionDigits:3}) : String(value);
const pct = value => `${(value*100).toFixed(1)}%`;
const selected = id => document.getElementById(id).value;
function legend(target, labels, palette) {
  document.getElementById(target).innerHTML = labels.map(label => `<span><i class="key" style="background:${palette[label]}"></i>${escapeText(label)}</span>`).join("");
}
function download(name, text, type="text/csv;charset=utf-8") {
  const url = URL.createObjectURL(new Blob([text],{type}));
  const link = document.createElement("a"); link.href=url; link.download=name;
  document.body.append(link); link.click(); link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function csv(rows) {
  if (!rows.length) return "";
  const fields=Object.keys(rows[0]);
  const cell=v=>`"${String(v??"").replace(/"/g,'""')}"`;
  return [fields.map(cell).join(","),...rows.map(row=>fields.map(k=>cell(row[k])).join(","))].join("\n")+"\n";
}
function source(id, rows) {
  chartRows.set(id,rows);
  const target=document.getElementById(`${id}-source`);
  if (!target) return;
  const fields=rows.length ? Object.keys(rows[0]) : [];
  target.innerHTML=`<summary>Source data · ${rows.length.toLocaleString("en-US")} rows</summary><p class="small muted">Current selection. ${rows.length>100 ? "The first 100 rows are displayed; the CSV contains every selected row." : "All selected rows are displayed."}</p><button type="button" data-download="${id}">Download selected CSV</button><div class="data-preview"><table><caption class="small">${escapeText(id.replaceAll("-"," "))}</caption><thead><tr>${fields.map(k=>`<th scope="col">${escapeText(k)}</th>`).join("")}</tr></thead><tbody>${rows.slice(0,100).map(row=>`<tr>${fields.map(k=>`<td>${escapeText(fmt(row[k]))}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
function svg(id, width, height, content, label) {
  document.getElementById(id).innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeText(label)}"><title>${escapeText(label)}</title>${content}</svg>`;
}
function text(x,y,value,anchor="start",cls="chart-label") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}">${escapeText(value)}</text>`;
}
function lineAxes(width,height,maxX,maxY,xLabel,yLabel,integerX=false,integerY=false) {
  const l=66,r=width-24,t=24,b=height-58;
  let content="";
  const yTicks=integerY ? Array.from({length:Math.floor(maxY)+1},(_,i)=>i) : Array.from({length:5},(_,i)=>Math.round(maxY*i/4));
  const xTicks=integerX ? Array.from({length:Math.floor(maxX)+1},(_,i)=>i) : Array.from({length:5},(_,i)=>Math.round(maxX*i/4));
  for(const value of [...new Set(yTicks)]) {
    const y=b-(b-t)*value/maxY;
    content+=`<line x1="${l}" x2="${r}" y1="${y}" y2="${y}" class="gridline"/>`;
    content+=text(l-10,y+4,fmt(value),"end");
  }
  for(const value of [...new Set(xTicks)]) {
    const x=l+(r-l)*value/maxX;
    content+=text(x,b+24,fmt(value),"middle");
  }
  content+=text((l+r)/2,height-8,xLabel,"middle");
  content+=text(l,14,yLabel);
  return {content,l,r,t,b};
}
function drawDistribution() {
  const choice=selected("distribution-collection");
  const labels=choice==="All" ? collections : [choice];
  const rows=Q.distribution.filter(r=>labels.includes(r.collection));
  const bands=[...new Set(rows.map(r=>r.band))];
  const width=950,height=370,l=66,r=925,t=25,b=310;
  let content="";
  const maxY=Math.max(.1,...rows.map(r=>r.levelShare))*1.12;
  for(let i=0;i<=4;i++) {
    const y=b-(b-t)*i/4;
    content+=`<line x1="${l}" x2="${r}" y1="${y}" y2="${y}" class="gridline"/>`+text(l-10,y+4,pct(maxY*i/4),"end");
  }
  const slot=(r-l)/bands.length,bar=slot*.72/labels.length;
  bands.forEach((band,i)=>{
    labels.forEach((collection,j)=>{
      const row=rows.find(v=>v.band===band&&v.collection===collection);
      const h=row.levelShare/maxY*(b-t),x=l+i*slot+slot*.14+j*bar;
      content+=`<rect x="${x}" y="${b-h}" width="${bar-3}" height="${h}" fill="${colors[collection]}" tabindex="0" aria-label="${escapeText(`${collection}, ${band}: ${row.count}/${row.n}, ${pct(row.levelShare)}`)}"><title>${escapeText(`${collection} · ${band}: ${row.count}/${row.n} (${pct(row.levelShare)})`)}</title></rect>`;
    });
    content+=text(l+(i+.5)*slot,b+25,band,"middle");
  });
  content+=text((l+r)/2,height-8,"Policy inputs to level completion","middle");
  svg("distribution-chart",width,height,content,"Distribution of recorded inputs to completed levels");
  legend("distribution-legend",labels,colors); source("distribution",rows);
}
function drawProfile() {
  const choice=selected("profile-collection");
  const labels=choice==="All" ? collections : [choice];
  const rows=Q.profile.filter(r=>labels.includes(r.collection));
  const width=950,height=390,maxX=Math.max(...rows.map(r=>r.level)),maxY=Math.max(...rows.map(r=>r.median))*1.12;
  const axes=lineAxes(width,height,maxX,maxY,"Native level","Median policy inputs",true);
  let content=axes.content;
  const x=v=>axes.l+(axes.r-axes.l)*v/maxX,y=v=>axes.b-(axes.b-axes.t)*v/maxY;
  labels.forEach(collection=>{
    const group=rows.filter(r=>r.collection===collection);
    content+=`<polyline fill="none" stroke="${colors[collection]}" stroke-width="2.5" points="${group.map(r=>`${x(r.level)},${y(r.median)}`).join(" ")}"/>`;
    group.forEach(row=>{content+=`<circle cx="${x(row.level)}" cy="${y(row.median)}" r="5" fill="${colors[collection]}" tabindex="0" aria-label="${escapeText(`${collection}, level ${row.level}, median ${row.median}, n=${row.n}`)}"><title>${escapeText(`${collection} · L${row.level}: median ${row.median}, n=${row.n}`)}</title></circle>`;});
  });
  svg("profile-chart",width,height,content,"Recorded median inputs by native level"); legend("profile-legend",labels,colors); source("profile",rows);
}
function stacked(id, groups, rows, groupKey, categoryKey, categories, valueKey, palette) {
  const width=950,l=groupKey==="collection" ? 165 : 110,r=925,top=26,rowHeight=30,height=top+groups.length*rowHeight+54;
  let content="";
  for(let i=0;i<=4;i++) {
    const x=l+(r-l)*i/4;
    content+=`<line x1="${x}" x2="${x}" y1="15" y2="${height-45}" class="gridline"/>`+text(x,height-23,`${i*25}%`,"middle");
  }
  groups.forEach((group,i)=>{
    const y=top+i*rowHeight; let left=l;
    content+=text(l-12,y+15,String(group).toUpperCase(),"end");
    categories.forEach(category=>{
      const row=rows.find(v=>String(v[groupKey])===String(group)&&v[categoryKey]===category);
      if(!row) return;
      const value=row[valueKey],w=value*(r-l);
      content+=`<rect x="${left}" y="${y}" width="${w}" height="21" fill="${palette[category]}" tabindex="0" aria-label="${escapeText(`${group}, ${category}: ${pct(value)}`)}"><title>${escapeText(`${group} · ${category}: ${pct(value)}${row.actions!==undefined ? ` (${row.actions} inputs)` : ""}`)}</title></rect>`;
      left+=w;
    });
  });
  svg(`${id}-chart`,width,height,content,`${id.replaceAll("-"," ")}: shares within each group`); source(id,rows);
}
function drawMix() {
  const weighted=selected("mix-denominator")==="game";
  stacked("mix",collections,Q[weighted ? "weighted_mix" : "mix"],"collection","mode",modes,weighted ? "meanGameShare" : "actionShare",modeColors);
  legend("mix-legend",modes,modeColors);
}
function drawLevelMix() {
  const rows=Q.by_level_mix.filter(r=>r.collection===selected("level-mix-collection"));
  stacked("level-mix",[...new Set(rows.map(r=>r.level))],rows,"level","mode",modes,"actionShare",modeColors);
  legend("level-mix-legend",modes,modeColors);
}
function drawGameMix() {
  const rows=Q.game_input.filter(r=>r.collection===selected("game-mix-collection"));
  const inputs=[...new Set(rows.map(r=>r.input))];
  const palette=Object.fromEntries(inputs.map((input,i)=>[input,["#3579bc","#5ba3df","#83c7ff","#c1e2ff","#ef64b4","#ffdc00","#999999"][i]]));
  stacked("game-mix",[...new Set(rows.map(r=>r.game))],rows,"game","input",inputs,"inputShare",palette);
  legend("game-mix-legend",inputs,palette);
}
function drawHeat() {
  const rows=Q.synthetic_heat.filter(r=>r.collection===selected("heat-collection"));
  const games=[...new Set(rows.map(r=>r.game))],levels=Math.max(...rows.map(r=>r.level));
  const width=650,l=80,top=38,cw=(width-l-20)/levels,rh=28,height=top+rh*games.length+38;
  let content="";
  for(let level=1;level<=levels;level++) content+=text(l+(level-.5)*cw,22,`L${level}`,"middle");
  games.forEach((game,i)=>{
    content+=text(l-12,top+i*rh+18,game.toUpperCase(),"end");
    rows.filter(r=>r.game===game).forEach(row=>{
      const k=Math.min(1,row.actions/100),fill=`rgb(${Math.round(33+195*k)},${Math.round(26+32*k)},${Math.round(32+130*k)})`;
      const x=l+(row.level-1)*cw,y=top+i*rh;
      content+=`<rect x="${x}" y="${y}" width="${cw-3}" height="${rh-3}" fill="${fill}"><title>${game.toUpperCase()} L${row.level}: ${row.actions} policy inputs</title></rect>`;
      content+=text(x+cw/2,y+18,row.actions,"middle","chart-value");
    });
  });
  svg("heat-chart",width,height,content,"Successful synthetic level action counts; color saturates at 100"); source("heat",rows);
}
function drawProgress() {
  const game=selected("progress-game"),rows=Q.progress.filter(r=>r.game===game);
  const width=950,height=390,maxX=Math.max(1,...rows.map(r=>r.actions)),maxY=Math.max(...rows.map(r=>r.completed));
  const axes=lineAxes(width,height,maxX,maxY,"Cumulative policy inputs","Completed levels",false,true);
  const x=v=>axes.l+(axes.r-axes.l)*v/maxX,y=v=>axes.b-(axes.b-axes.t)*v/maxY;
  let content=axes.content,path="";
  rows.forEach((row,i)=>{path+=i ? `H${x(row.actions)} V${y(row.completed)} ` : `M${x(row.actions)} ${y(row.completed)} `;});
  content+=`<path d="${path}" fill="none" stroke="${colors[rows[0].collection]}" stroke-width="3"/>`;
  rows.forEach(row=>{content+=`<circle cx="${x(row.actions)}" cy="${y(row.completed)}" r="4" fill="${colors[row.collection]}" tabindex="0" aria-label="${row.actions} inputs, ${row.completed} completed levels"><title>${row.actions} inputs · ${row.completed} completed levels</title></circle>`;});
  svg("progress-chart",width,height,content,`${game.toUpperCase()} source-informed AI action progression`);
  document.getElementById("progress-readout").textContent=`${game.toUpperCase()} · ${rows[0].collection} · ${maxX} inputs · ${maxY} completed levels${rows[0].collection==="Studio V2" ? " · concatenated successful level excerpts" : " · recorded full-run progression"}`;
  source("progress",rows);
}
function drawClicks() {
  const rows=Q.click_map.filter(r=>r.collection===selected("click-collection"));
  const width=600,height=585,l=70,top=25,cell=62;let content="";
  rows.forEach(row=>{
    const x=parseInt(row.x,10)/8,y=parseInt(row.y,10)/8,k=Math.min(1,row.clickShare/.15);
    content+=`<rect x="${l+x*cell}" y="${top+y*cell}" width="${cell-2}" height="${cell-2}" fill="rgb(${Math.round(33+195*k)},${Math.round(26+32*k)},${Math.round(32+130*k)})" tabindex="0" aria-label="${escapeText(`x ${row.x}, y ${row.y}: ${row.count} clicks, ${pct(row.clickShare)}`)}"><title>${escapeText(`x ${row.x} · y ${row.y}: ${row.count} clicks (${pct(row.clickShare)})`)}</title></rect>`;
  });
  for(let i=0;i<8;i++) {content+=text(l+(i+.5)*cell,top+8*cell+23,`${i*8}`,"middle"); content+=text(l-13,top+(i+.5)*cell+4,`${i*8}`,"end");}
  content+=text(l+4*cell,height-8,"Native x coordinate (8-pixel bins)","middle");
  svg("click-chart",width,height,content,"Click-location aggregate heat map, native top-left origin; color saturates at 15%"); source("click",rows);
}
function drawReviews() {
  const collection=selected("reviews-collection"),needle=selected("reviews-search").trim().toLowerCase(),sort=selected("reviews-sort");
  const rows=Q.game_reviews.filter(r=>(collection==="All"||sourceNames[r.source]===collection)&&`${r.game} ${r.title} ${r.family}`.toLowerCase().includes(needle));
  rows.sort((a,b)=>sort==="game" ? a.game.localeCompare(b.game) : b[sort]-a[sort]||a.game.localeCompare(b.game));
  document.getElementById("reviews-count").textContent=`${rows.length} games · provisional source-informed assessments`;
  document.getElementById("reviews-body").innerHTML=rows.map(r=>`<tr><th scope="row">${escapeText(r.game.toUpperCase())}<br><span class="muted small">${escapeText(sourceNames[r.source])}</span></th><td>${escapeText(r.family)}</td><td class="num">${r.planning}</td><td class="num">${r.discovery}</td><td class="num">${r.decoding}</td><td class="num">${fmt(r.median_level_actions)}</td><td class="num">${fmt(r.late_mean_actions)}</td><td class="review-note">${escapeText(r.review_note)}</td></tr>`).join("");
  source("reviews",rows);
}
const controls={"distribution-collection":drawDistribution,"profile-collection":drawProfile,"mix-denominator":drawMix,"level-mix-collection":drawLevelMix,"game-mix-collection":drawGameMix,"heat-collection":drawHeat,"progress-game":drawProgress,"click-collection":drawClicks,"reviews-collection":drawReviews,"reviews-sort":drawReviews};
for(const [id,fn] of Object.entries(controls)) document.getElementById(id).addEventListener("change",fn);
document.getElementById("reviews-search").addEventListener("input",drawReviews);
document.addEventListener("click",event=>{
  const button=event.target.closest("[data-download]");
  if(button) download(`arc3-analysis-${button.dataset.download}.csv`,csv(chartRows.get(button.dataset.download)||[]));
});
document.getElementById("download-summary").addEventListener("click",()=>download("arc3-analysis-summary.json",JSON.stringify(reportData,null,2)+"\n","application/json"));
for(const id of ["distribution-collection","profile-collection","level-mix-collection","click-collection"]) {
  document.getElementById(id).innerHTML=(id.startsWith("distribution")||id.startsWith("profile") ? '<option value="All">All collections</option>' : "")+collections.map(c=>`<option>${c}</option>`).join("");
}
for(const id of ["game-mix-collection","heat-collection","reviews-collection"]) {
  document.getElementById(id).innerHTML=(id==="reviews-collection" ? '<option value="All">All synthetic</option>' : "")+collections.slice(0,3).map(c=>`<option>${c}</option>`).join("");
}
document.getElementById("progress-game").innerHTML=[...new Set(Q.progress.map(r=>r.game))].map(g=>`<option value="${escapeText(g)}">${escapeText(g.toUpperCase())}</option>`).join("");
for(const id of ["game-mix-collection","heat-collection","level-mix-collection","click-collection"]) document.getElementById(id).value="Studio V2";
document.getElementById("progress-game").value="v220";
[drawDistribution,drawProfile,drawMix,drawLevelMix,drawGameMix,drawHeat,drawProgress,drawClicks,drawReviews].forEach(fn=>fn());
