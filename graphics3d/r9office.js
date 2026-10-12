// V7.9 r6: R9 office / architecture / airflow layer of the 3D page (R9 OFFICE-B1-R9 developer handover, 2026-10-12).
// Source: the R9 code that the handover inserts into the 3D page closure (refinement.js, office.js, furnishing_r5/r7.js,
// r4-r9_graphics.js). Bundle-internal names were renamed scope-aware to the scene79.js names (S.<name>) or THREE.<class>;
// the logic is unchanged except where marked 'r6:'. installR9(S) runs once after the panels exist (scene79.js).
import * as THREE from 'three';

export function installR9(S){

/* Detail additions inside the original Three.js closure. All objects stay in
   their existing equipment or floor group so isolation and alarms still work. */
var detailMeshCount=0;
function detail(geometry,material,parent,position,rotation){
  var mesh=S.mesh(geometry,material,parent,position,rotation);
  detailMeshCount++;return mesh;
}
var sealMat=new THREE.MeshStandardMaterial({color:'#737b7e',roughness:.85,metalness:.08});
var boltMat=new THREE.MeshStandardMaterial({color:'#8b9396',roughness:.48,metalness:.7});
var faceMat=new THREE.MeshStandardMaterial({color:'#cbd4d6',roughness:.2,metalness:.05});
var addedMaterials=[sealMat,boltMat,faceMat];
for(var eqid in S.EQ){
  var unit=S.EQ[eqid],group=unit.g,eq=unit.e,L=S.mm(eq.L),H=S.mm(eq.H),W=S.mm(eq.W);
  if(eq.type==='chiller'){
    // Bolted water-box covers and shell insulation seams.
    for(var end of [-1,1]){
      for(var shell of [{h:1.08,z:.18,r:.44},{h:.62,z:-.22,r:.38}]){
        detail(S.cyl(shell.r*.96,.018,40),sealMat,group,new THREE.Vector3(end*L*.474,shell.h,shell.z),[0,0,Math.PI/2]);
        for(var k=0;k<12;k++){
          var ang=k*Math.PI/6;
          detail(S.cyl(.018,.035,6),boltMat,group,new THREE.Vector3(end*L*.482,shell.h+Math.sin(ang)*shell.r*.88,shell.z+Math.cos(ang)*shell.r*.88),[0,0,Math.PI/2]);
        }
      }
    }
    for(var seam of [-.25,0,.25]){
      detail(new THREE.TorusGeometry(.425,.006,6,40),sealMat,group,new THREE.Vector3(L*seam,1.08,.18),[0,Math.PI/2,0]);
      detail(new THREE.TorusGeometry(.365,.006,6,40),sealMat,group,new THREE.Vector3(L*seam,.62,-.22),[0,Math.PI/2,0]);
    }
    detail(S.box(.16,.05,.012),sealMat,group,new THREE.Vector3(L*.5+.189,1.05,.55),[0,Math.PI/2,0]);
    var plate=S.textSprite(eq.id,27,'#35474f',null);plate.position.set(L*.5+.196,1.12,.1);plate.scale.set(.32,.16,1);plate.rotation.y=Math.PI/2;group.add(plate);
  } else if(eq.type==='pump'){
    // Motor terminal box and holding-down bolts; painted casing remains blue-grey.
    detail(S.box(.22,.12,.16,.01),S.MAT.motor,group,new THREE.Vector3(L*.22,.86,0));
    for(var sx of [-1,1]) for(var sz of [-1,1])detail(S.cyl(.018,.02,6),boltMat,group,new THREE.Vector3(sx*L*.42,.375,sz*W*.3));
    detail(S.cyl(.008,.2,8),S.MAT.galv,group,new THREE.Vector3(-L*.3,1.18,0));
    detail(S.cyl(.045,.025,20),S.MAT.galv,group,new THREE.Vector3(-L*.3,1.29,0),[Math.PI/2,0,0]);
    detail(S.cyl(.038,.028,20),faceMat,group,new THREE.Vector3(-L*.3,1.29,.016),[Math.PI/2,0,0]);
    detail(S.box(.005,.042,.004),sealMat,group,new THREE.Vector3(-L*.3,1.30,.034),[0,0,-.5]);
  } else if(eq.type==='ct'){
    // Panel joints, fastening heads and actual steel access walkway.
    for(var xx=-L*.4;xx<L*.5;xx+=.52){
      for(var zz of [-W/2-.044,W/2+.044]){
        detail(S.box(.016,H-.66,.012),sealMat,group,new THREE.Vector3(xx,H/2+.28,zz));
        for(var yy of [.7,H-.18])detail(S.cyl(.012,.008,6),boltMat,group,new THREE.Vector3(xx,yy,zz),[Math.PI/2,0,0]);
      }
    }
    for(var slat=0;slat<10;slat++)detail(S.box(L,.016,.02),S.MAT.galv,group,new THREE.Vector3(0,H+.024,W/2+.12+slat*.035));
  } else if(eq.type==='ahu'){
    for(var door of [-.32,.05,.35]){
      detail(S.box(.012,H*.88,.014),sealMat,group,new THREE.Vector3(L*door,H/2,W/2+.032));
      detail(S.box(.012,.16,.04),S.MAT.black,group,new THREE.Vector3(L*door+.08,H*.5,W/2+.05));
    }
  }
  addedMaterials.forEach(function(material){unit.mats.add(material.clone());});
}
// Architectural detail follows the existing 64 m x 40 m reference footprint.
var facadeMat=new THREE.MeshStandardMaterial({color:'#d6d3ca',roughness:.85,metalness:.03});
var frameMat=new THREE.MeshStandardMaterial({color:'#68767e',roughness:.65,metalness:.5});
for(var floorNumber=1;floorNumber<=S.BLD.floors;floorNumber++){
  var floorDetail=new THREE.Group;S.LAYER.shell.add(floorDetail);S.onFloor(floorNumber,floorDetail);
  var baseHeight=S.zOf(floorNumber),floorHeight=(floorNumber===1?S.BLD.f1_h:S.BLD.typ_h)-S.BLD.slab;
  // Spandrel at slab edge, separate aluminium transoms and facade fins.
  for(var side of [0,S.BLD.y]){
    detail(S.box(S.mm(S.BLD.x),.34,.08),facadeMat,floorDetail,S.P3(S.BLD.x/2,side,baseHeight+260));
    detail(S.box(S.mm(S.BLD.x),.055,.08),frameMat,floorDetail,S.P3(S.BLD.x/2,side,baseHeight+floorHeight*.58));
    for(var gridX=2000;gridX<S.BLD.x;gridX+=8000)
      detail(S.box(.12,S.mm(floorHeight),.32),facadeMat,floorDetail,S.P3(gridX,side,baseHeight+floorHeight/2));
  }
  for(var sideX of [0,S.BLD.x]){
    detail(S.box(.08,.34,S.mm(S.BLD.y)),facadeMat,floorDetail,S.P3(sideX,S.BLD.y/2,baseHeight+260));
    detail(S.box(.08,.055,S.mm(S.BLD.y)),frameMat,floorDetail,S.P3(sideX,S.BLD.y/2,baseHeight+floorHeight*.58));
  }
}
// Roof joints and practical perimeter coping.
var roofDetail=new THREE.Group;S.LAYER.shell.add(roofDetail);S.onFloor(9,roofDetail);
for(var seamX=4000;seamX<S.BLD.x;seamX+=4000)detail(S.box(.018,.006,S.mm(S.BLD.y)),sealMat,roofDetail,S.P3(seamX,S.BLD.y/2,S.ROOFZ+4));
for(var seamY=4000;seamY<S.BLD.y;seamY+=4000)detail(S.box(S.mm(S.BLD.x),.006,.018),sealMat,roofDetail,S.P3(S.BLD.x/2,seamY,S.ROOFZ+4));
for(var edge of [[S.BLD.x/2,0,S.BLD.x,380],[S.BLD.x/2,S.BLD.y,S.BLD.x,380],[0,S.BLD.y/2,380,S.BLD.y],[S.BLD.x,S.BLD.y/2,380,S.BLD.y]])
  detail(S.box(S.mm(edge[2]),.045,S.mm(edge[3])),S.MAT.galv,roofDetail,S.P3(edge[0],edge[1],S.ROOFZ+S.BLD.parapet+20));
// Entrance canopy is a visual reference detail, not an as-built structural element.
var entry=new THREE.Group;S.LAYER.shell.add(entry);S.onFloor(1,entry);
detail(S.box(10,.18,3.2),facadeMat,entry,S.P3(54000,-1400,3600));
for(var postX of [50000,58000])detail(S.box(.18,3.55,.18),frameMat,entry,S.P3(postX,-2500,1775));
detail(S.box(11,.1,4.2),S.MAT.concrete,entry,S.P3(54000,-1800,-50));
var note=document.createElement('div');note.className='material-note';note.textContent='Reference geometry · reference material colours, not as-built';
document.querySelector('aside section').appendChild(note);
// Secondary controls stay available behind compact disclosures.
var sysHeading=Array.from(document.querySelector('aside section').querySelectorAll('h2')).find(function(h){return h.textContent.includes('Future systems');});
if(sysHeading){var sysDetails=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Future systems';sysHeading.replaceWith(sysDetails);sysDetails.appendChild(summary);sysDetails.appendChild(S.$('sysl'));}
var simHeading=S.$('sim').querySelector('h2');
if(simHeading){var simDetails=document.createElement('details'),simSummary=document.createElement('summary');simSummary.textContent='Alarm simulation (DEMO)';simHeading.remove();simDetails.appendChild(simSummary);while(S.$('sim').firstChild)simDetails.appendChild(S.$('sim').firstChild);S.$('sim').appendChild(simDetails);}
var zoneRow=document.querySelector('.zrow'),zoneControl=document.querySelector('[data-layer="zones"]');
if(zoneRow&&zoneControl){zoneRow.style.display='none';zoneControl.addEventListener('change',function(){zoneRow.style.display=zoneControl.checked?'':'none';});}
// Zone tint and future-system markers remain available through layers, off initially.
for(var initialLayer of ['zones','systems']){
  var cb=document.querySelector('[data-layer="'+initialLayer+'"]');
  if(cb){cb.checked=false;S.LAYER[initialLayer].visible=false;}
}
var spareRow=document.createElement('label');spareRow.style.display='block';spareRow.style.marginTop='7px';
spareRow.innerHTML='<input type="checkbox" id="showSpare"> Show empty (not installed) slots';document.querySelector('aside section').appendChild(spareRow);
function updateSpareVisibility(){
  var show=S.$('showSpare').checked;
  for(var id in S.EQ)if(S.EQ[id].ghost)S.EQ[id].g.visible=show&&(!S.ISO||S.FSEL==='all'||S.FSEL==='roof'||S.EQ[id].e.floor==+S.FSEL||(!S.EQ[id].e.floor&&S.FSEL==='1'));
  for(var id in S.PIPE)if(S.PIPE[id].ghost)S.PIPE[id].g.visible=show;
}
var originalOv=S.updateGhosts;S.updateGhosts=function(){originalOv();updateSpareVisibility();};
S.$('showSpare').onchange=function(){S.applyFloor();updateSpareVisibility();};
document.querySelectorAll('[data-view]').forEach(function(btn){btn.addEventListener('click',function(){
  document.querySelectorAll('[data-view]').forEach(function(b){b.classList.toggle('active',b===btn);});
  var shellControl=document.querySelector('[data-layer="shell"]');
  shellControl.checked=!['plant','pumps','room','floor'].includes(btn.dataset.view);S.LAYER.shell.visible=shellControl.checked;
  // Clear equipment selection when changing the view.
  S.$('info').className='';
});});
window.__DESIGN={version:'2026-10-10',detailMeshCount:detailMeshCount,inspect:function(){return {equipment:Object.keys(S.EQ).length,pipes:Object.keys(S.PIPE).length,detailMeshCount:detailMeshCount,mode:S.DEMO?'DEMO':document.getElementById('mode').textContent,camera:S.camera.position.toArray(),materials:{chiller:S.MAT.almond.color.getHexString(),pump:S.MAT.motor.color.getHexString(),tower:S.MAT.frp.color.getHexString()},renderer:S.renderer.info.render,triangles:S.renderer.info.render.triangles};}};
(function(){
var plan=window.OFFICE_DESIGN,rooms=plan.rooms,storeys={},boxes=[],omitted=[];
var mat={
 concrete:new THREE.MeshStandardMaterial({color:'#9f9d94',map:S.T.concrete,roughness:.92}),wall:new THREE.MeshStandardMaterial({color:'#d0c9b9',roughness:.93}),
 frame:new THREE.MeshStandardMaterial({color:'#263b45',roughness:.45,metalness:.65}),metal:new THREE.MeshStandardMaterial({color:'#89999e',roughness:.38,metalness:.75}),
 carpet:new THREE.MeshStandardMaterial({color:'#6b7473',roughness:1}),tile:new THREE.MeshStandardMaterial({color:'#a39c8b',roughness:.67}),wood:new THREE.MeshStandardMaterial({color:'#b59872',roughness:.75}),
 chair:new THREE.MeshStandardMaterial({color:'#273c46',roughness:.86}),sofa:new THREE.MeshStandardMaterial({color:'#697068',roughness:.96}),screen:new THREE.MeshStandardMaterial({color:'#16262c',emissive:'#18475a',emissiveIntensity:.25}),
 duct:new THREE.MeshStandardMaterial({color:'#7f9199',metalness:.72,roughness:.38}),returnDuct:new THREE.MeshStandardMaterial({color:'#7b817d',metalness:.65,roughness:.43}),
 insulated:new THREE.MeshStandardMaterial({color:'#323d40',roughness:.88}),SA:new THREE.MeshStandardMaterial({color:'#47c7f5',roughness:.6}),RA:new THREE.MeshStandardMaterial({color:'#bb9bea',roughness:.65}),
 OA:new THREE.MeshStandardMaterial({color:'#43d19b',roughness:.62}),KE:new THREE.MeshStandardMaterial({color:'#7d6055',roughness:.7}),MA:new THREE.MeshStandardMaterial({color:'#77999c',roughness:.6}),TE:new THREE.MeshStandardMaterial({color:'#f28d64',roughness:.7}),
 EA:new THREE.MeshStandardMaterial({color:'#f28d64',roughness:.65}),TA:new THREE.MeshStandardMaterial({color:'#879c94',roughness:.65}),
 PA:new THREE.MeshStandardMaterial({color:'#6f8f8b',roughness:.65}),PE:new THREE.MeshStandardMaterial({color:'#8b8178',roughness:.65}),
 glass:new THREE.MeshStandardMaterial({color:'#b0c3c1',transparent:true,opacity:.18,depthWrite:false,roughness:.15,metalness:.15,side:THREE.DoubleSide}),
 luminaire:new THREE.MeshStandardMaterial({color:'#fff0ce',emissive:'#ffe1ad',emissiveIntensity:2.2,roughness:.6}),
 foliage:new THREE.MeshStandardMaterial({color:'#334e3d',roughness:1}),pot:new THREE.MeshStandardMaterial({color:'#786b59',roughness:.9}),blue:new THREE.MeshStandardMaterial({color:'#315e7b',metalness:.45,roughness:.45})
};
for(var k in mat)mat[k].envMapIntensity=.035;
// Repeatable fine texture, rather than baked illustration: geometry remains editable.
mat.wood.map=S.canvasTex(256,256,function(c,w,h){c.fillStyle='#b49b80';c.fillRect(0,0,w,h);for(var i=0;i<100;i++){c.strokeStyle=i%3?'rgba(64,42,23,.10)':'rgba(235,221,199,.16)';c.beginPath();c.moveTo(0,i*3);c.bezierCurveTo(80,i*3+2,170,i*3-2,256,i*3+1);c.stroke();}},[2,2]);
mat.carpet.map=S.canvasTex(128,128,function(c,w,h){c.fillStyle='#bbbbbb';c.fillRect(0,0,w,h);for(var y=0;y<h;y+=2)for(var x=0;x<w;x+=2){c.fillStyle=(x+y)%4?'#999999':'#cccccc';c.fillRect(x,y,1,1);}},[16,16]);
var height=function(f){return f===0?6:f===1?5.5:4.2;},base=function(f){return f===0?-6:f===1?0:f===9?34.9:5.5+(f-2)*4.2;};
function collide(a,b,gap){return [0,1,2].every(function(k){return a[k]<b[k+3]+(gap||0)&&a[k+3]>b[k]-(gap||0);});}
function bounds(x,y,z,w,h,d,angle){var c=Math.abs(Math.cos(angle||0)),s=Math.abs(Math.sin(angle||0)),ww=w*c+d*s,dd=w*s+d*c;return [x-ww/2,z-dd/2,y-h/2,x+ww/2,z+dd/2,y+h/2];}
function obstacles(f){return plan.columns.filter(function(c){return c.floor===f;});}
function batch(parent,f,kind,absolute){var buckets={},b=absolute?0:base(f);return {
 box:function(key,x,y,z,w,h,d,angle,protect){if(w<.001||h<.001||d<.001)return;var box=bounds(x,y+b,z,w,h,d,angle);
  if(protect&&obstacles(f).some(function(o){return collide(box,o.box,.025);})){omitted.push({floor:f,kind:kind,material:key,box:box});return;}
  (buckets[key]||(buckets[key]=[])).push([x,y,-z,w,h,d,angle||0]);if(kind!=='structure'&&kind!=='envelope')boxes.push({floor:f,kind:kind==='furniture'&&h<=.04&&y<.1?'finish':kind,material:key,box:box});
 },flush:function(){var cube=new THREE.BoxGeometry(1,1,1),p=cube.attributes.position,n=cube.attributes.normal,u=cube.attributes.uv,idx=cube.index;
  for(var key in buckets){var verts=[],norm=[],uv=[],index=[];buckets[key].forEach(function(r){var c=Math.cos(r[6]),s=Math.sin(r[6]),off=verts.length/3;for(var j=0;j<p.count;j++){var x=p.getX(j)*r[3],z=p.getZ(j)*r[5];verts.push(r[0]+x*c+z*s,r[1]+p.getY(j)*r[4],r[2]-x*s+z*c);x=n.getX(j);z=n.getZ(j);norm.push(x*c+z*s,n.getY(j),-x*s+z*c);uv.push(u.getX(j),u.getY(j));}for(var j=0;j<idx.count;j++)index.push(off+idx.getX(j));});
   var geo=new THREE.BoxGeometry(1,1,1);geo.setAttribute('position',new p.constructor(verts,3));geo.setAttribute('normal',new n.constructor(norm,3));geo.setAttribute('uv',new u.constructor(uv,2));geo.setIndex(index);geo.clearGroups();geo.computeBoundingSphere();var mesh=S.mesh(geo,mat[key].clone(),parent);mesh.userData.designKind=kind;
  }cube.dispose();}
};}
function flatLabel(parent,text,x,py,z,w){var c=document.createElement('canvas');c.width=512;c.height=96;var ctx=c.getContext('2d');ctx.textAlign='center';ctx.fillStyle='#e9e0cd';ctx.font='600 34px Segoe UI';ctx.fillText(text,256,62);var tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;var mesh=S.mesh(new THREE.PlaneGeometry(w,w*.1875),new THREE.MeshBasicMaterial({map:tex,transparent:true,depthWrite:false}),parent,new THREE.Vector3(x,py,-z),[-Math.PI/2,0,0]);return mesh;}
function wall(b,f,x0,z0,x1,z1,door,glazed){var len=Math.hypot(x1-x0,z1-z0),ux=(x1-x0)/len,uz=(z1-z0)/len,angle=Math.atan2(z1-z0,x1-x0),cuts=[];
 // Walls terminate beside columns; they never bury the concrete section.
 obstacles(f).forEach(function(o){var cx=(o.box[0]+o.box[3])/2,cz=(o.box[1]+o.box[4])/2,t=(cx-x0)*ux+(cz-z0)*uz,dist=Math.abs((cx-x0)*uz-(cz-z0)*ux);if(dist<.39&&t>-.4&&t<len+.4)cuts.push([Math.max(0,t-.4),Math.min(len,t+.4)]);});
 if(door!==undefined)cuts.push([Math.max(.2,door),Math.min(len-.2,door+1.1)]);
 cuts.sort(function(a,b){return a[0]-b[0];});var spans=[],prev=0;cuts.forEach(function(c){if(c[0]>prev)spans.push([prev,c[0]]);prev=Math.max(prev,c[1]);});if(prev<len)spans.push([prev,len]);
 function piece(a,c,py,h,key,d){if(c-a<.02)return;b.box(key,x0+ux*(a+c)/2,py,z0+uz*(a+c)/2,c-a,h,d||.12,angle,true);}
 spans.forEach(function(s){if(glazed){piece(s[0],s[1],.22,.44,'wall');piece(s[0],s[1],1.65,2.36,'glass',.025);piece(s[0],s[1],2.85,.055,'frame',.065);piece(s[0],s[0]+.04,1.62,2.55,'frame',.07);piece(s[1]-.04,s[1],1.62,2.55,'frame',.07);}else piece(s[0],s[1],1.45,2.9,'wall');piece(s[0],s[1],.06,.12,'frame',.13);});
 if(door!==undefined){var a=Math.max(.2,door),c=Math.min(len-.2,door+1.1);piece(a,c,2.65,.5,'wall');piece(a+.03,c-.03,1.08,2.14,glazed?'glass':'wood',.045);piece(a,a+.04,1.13,2.26,'frame',.08);piece(c-.04,c,1.13,2.26,'frame',.08);piece(a,c,2.25,.045,'frame',.08);piece(c-.16,c-.10,1.05,.035,'metal',.13);}
}
function desk(b,x,z,meeting){var w=meeting?2.8:1.4,d=meeting?1.1:.7;b.box('wood',x,.74,z,w,.065,d,0,true);for(var xx of [-w*.38,w*.38])b.box('frame',x+xx,.36,z,.05,.7,d*.7,0,true);
 if(!meeting){b.box('screen',x,.98,z-.05,.45,.29,.035,0,true);b.box('frame',x,.83,z-.05,.12,.14,.08,0,true);b.box('chair',x,.43,z+.7,.45,.08,.43,0,true);b.box('chair',x,.68,z+.85,.45,.5,.06,0,true);}else for(var side of [-1,1])for(var xx of [-.85,.85]){b.box('chair',x+xx,.44,z+side*.9,.48,.08,.43,0,true);b.box('chair',x+xx,.70,z+side*1.07,.48,.48,.06,0,true);}
}
function plantPot(b,x,z){b.box('pot',x,.22,z,.4,.44,.4,0,true);b.box('foliage',x,.72,z,.66,.7,.6,0,true);}
// Function-specific rental interiors. Circulation stays between perimeter rooms and service core.
function workstation(b,x,z,angle){var c=Math.cos(angle||0),s=Math.sin(angle||0);function p(key,dx,h,dz,w,hh,dep){b.box(key,x+dx*c+dz*s,h,z-dx*s+dz*c,w,hh,dep,angle||0,true);}
 p('wood',0,.74,0,1.35,.06,.65);p('frame',-.5,.36,0,.05,.70,.48);p('frame',.5,.36,0,.05,.70,.48);p('screen',0,.98,-.1,.46,.28,.035);p('chair',0,.43,.67,.46,.08,.43);p('chair',0,.68,.84,.46,.48,.06);
}
function bench(b,x,z,n,angle){for(var i=0;i<n;i++)workstation(b,x+(i-(n-1)/2)*1.5,z,angle);}
function seat(b,x,z,angle){b.box('chair',x,.44,z,.48,.08,.45,angle||0,true);b.box('chair',x,.69,z+.18,.48,.48,.06,angle||0,true);}
function cabinet(b,x,z,w){b.box('wood',x,.52,z,w,1.0,.42,0,true);b.box('frame',x,.72,z+.22,w-.06,.025,.035,0,true);}
function sofa(b,x,z,w,angle){b.box('sofa',x,.38,z,w,.55,.85,angle||0,true);b.box('sofa',x,.74,z-.34,w,.65,.16,angle||0,true);}
function layoutOffice(b,r){var a=r.rect,x0=a[0],z0=a[1],x1=a[2],z1=a[3],cx=(x0+x1)/2,cz=(z0+z1)/2,k=r.layoutVariant;
 if(r.id==='G-REC'){b.box('wood',cx,.95,z0+1.3,4.6,.12,.85,0,true);b.box('wall',cx,.46,z0+1.3,4.4,.85,.75,0,true);workstation(b,x0+2,z1-2.2,0);workstation(b,x1-2,z1-2.2,0);sofa(b,cx,z0+3.3,2.4,0);return;}
 var west=x0<40&&r.floor>1,p=cz<18?z1-r.privateDepth_m:z0+r.privateDepth_m,lo=west?(cz<18?z0:p+.12):z0,hi=west?(cz<18?p-.12:z1):z1,mid=(lo+hi)/2;
 if(k===0){for(var zz of [lo+2.1,hi-2.4]){workstation(b,cx-.9,zz,0);workstation(b,cx+.9,zz,0);}cabinet(b,x0+.6,mid,1.0);}
 if(k===1){workstation(b,cx,lo+(r.id.endsWith('EN2')?3.3:2.0),Math.PI);sofa(b,cx,hi-1.6,2.7,0);b.box('wood',cx,.38,hi-2.8,1.25,.06,.65,0,true);cabinet(b,cx,lo+.5,2.5);}
 if(k===2){workstation(b,x0+1.1,lo+2.1,Math.PI/2);workstation(b,x1-1.1,hi-2.2,-Math.PI/2);b.box('wood',cx,.87,mid,2.5,.08,1.2,0,true);b.box('wall',x1-.25,1.55,mid,.05,1.0,2.2,0,true);}
 if(k===3){workstation(b,x0+1.4,lo+1.6,0);workstation(b,x1-1.4,hi-2.0,Math.PI);desk(b,cx,mid,true);cabinet(b,x0+.5,mid, .75);}
 if(k===4){for(var zz=lo+1.7;zz<hi-1.8;zz+=2.5){workstation(b,cx-.95,zz,Math.PI);workstation(b,cx+.95,zz,Math.PI);}b.box('screen',cx,1.8,lo+.20,1.9,1.1,.06,0,true);}
 if(k===5){workstation(b,cx,lo+1.9,0);workstation(b,cx,hi-2.0,Math.PI);sofa(b,x0+.7,mid,2.1,Math.PI/2);b.box('wood',x1-.75,.8,mid,.9,.07,2.1,0,true);}
 if(west){var pc=cz<18?(p+z1)/2:(z0+p)/2;if(k===1)workstation(b,cx,pc,0);else if(k===5){workstation(b,cx,pc,Math.PI/2);cabinet(b,x1-.4,pc,.6);}else desk(b,cx,pc,true);}
 plantPot(b,x1-.65,lo+.65);
}
function layoutMeeting(b,r){var a=r.rect,cx=(a[0]+a[2])/2,cz=(a[1]+a[3])/2,k=r.layoutVariant;
 if(k===0)desk(b,cx,cz,true);
 if(k===1){for(var x of [cx-1.45,cx+1.45])for(var z of [cz-.85,cz+.85])workstation(b,x,z,Math.PI);}
 if(k===2){b.box('wood',cx,.74,cz,2.2,.065,.9,0,true);for(var x of [cx-.7,cx+.7])seat(b,x,cz+.9,0);b.box('screen',cx,1.65,a[1]+.16,1.8,1.05,.06,0,true);}
 if(k===3){b.box('wood',cx,.9,cz,2.2,.065,1.2,0,true);for(var x of [cx-1.35,cx+1.35])seat(b,x,cz,Math.PI/2);b.box('wall',cx,1.7,a[3]-.15,2.5,1.1,.05,0,true);}
 if(k!==2)b.box('screen',cx,1.7,a[1]+.17,1.35,.75,.05,0,true);
}
function furnishRoom(b,r){var a=r.rect,x0=a[0],z0=a[1],x1=a[2],z1=a[3],cx=(x0+x1)/2,cz=(z0+z1)/2;
 if(r.r6)return furnishR6(b,r);
 if(r.kind==='office')return layoutOffice(b,r);if(r.kind==='meeting')return layoutMeeting(b,r);
 if(r.kind==='lobby'){if(r.id==='G-LOB'){b.box('wood',23,.9,5,5,.12,1.1,0,true);b.box('wall',23,.43,5,4.8,.8,1,0,true);for(var x of [6,13,20]){sofa(b,x,10.5,3.2,0);b.box('wood',x,.37,9.2,1.4,.06,.7,0,true);}plantPot(b,3,3);plantPot(b,28,12);}else{for(var x of [x0+3.2,x0+9,x1-3.2]){sofa(b,x,z0+2,2.4,0);b.box('wood',x,.4,cz,1.1,.06,.65,0,true);}sofa(b,cx,z1-1.2,3.4,Math.PI);plantPot(b,x1-.8,z0+.8);}}
 else if(r.kind==='dining'){for(var x=x0+3;x<x1-2;x+=4.8)for(var z=z0+2.4;z<z1-1.6;z+=3.7){if((Math.round(x)%3)===0){b.box('wood',x,.74,z,1.1,.07,.9,0,true);seat(b,x,z-.85,Math.PI);seat(b,x,z+.85,0);}else desk(b,x,z,true);}b.box('wood',cx,.94,z1-.65,14,.09,.65,0,true);for(var x=cx-6;x<cx+6;x+=1.5)seat(b,x,z1-1.5,0);}
 else if(r.kind==='kitchen'){var kx=r.id==='G-KITCH'?54:cx,w=Math.min(4,x1-x0-1);b.box('metal',kx,.86,cz,w,.10,.8,0,true);b.box('metal',kx,.42,cz,w-.1,.75,.7,0,true);b.box('metal',kx,2.8,cz,Math.min(4.4,x1-x0-.5),.55,1.1,0,true);b.box('chair',kx,.96,cz,r.layoutVariant%2?.5:.9,.035,.5,0,true);if(r.id==='G-KITCH'){cabinet(b,51,31,2);b.box('metal',54,.88,37,4,.08,.8,0,true);b.box('metal',56.3,1.0,37,.9,1.9,.8,0,true);}}
 else if(r.kind==='toilet'){if(r.id.endsWith('WC-A')){b.box('wall',x0+.9,.5,z1-1,.5,.5,.6,0,true);b.box('metal',x1-.6,.84,z0+.7,.65,.12,.45,0,true);}else{for(var x=x0+.8;x<x1-.5;x+=1.35){b.box('wall',x,.5,z1-.8,.4,.5,.55,0,true);b.box('metal',x,.85,z0+.55,.65,.12,.45,0,true);}}}
 else if(r.kind==='pantry'){cabinet(b,cx,z1-.45,x1-x0-.5);b.box('metal',x0+1,.95,z1-.45,.7,.05,.45,0,true);b.box('wood',cx,.9,cz,2.0,.08,.65,0,true);seat(b,cx-.5,z0+.7,0);seat(b,cx+.5,z0+.7,0);}
 else if(r.kind==='service'){if(r.id.includes('IT')){for(var x of [x0+.65,x1-.65])b.box('frame',x,1.0,cz,.6,1.9,.8,0,true);}else if(r.id==='G-WASH'){b.box('metal',cx,.88,z0+.7,3,.08,.8,0,true);b.box('metal',x1-1,.6,z1-1,1,1.1,1,0,true);}else{for(var x=x0+1;x<x1-.8;x+=1.8)cabinet(b,x,z1-.65,1.3);}}
 else if(r.kind==='stair')for(var step=0;step<12;step++)b.box('concrete',cx,.09+step*.18,z0+.4+step*.25,2,.18,.25,0,true);
}

function furnishR6(b,r){var a=r.rect,cx=(a[0]+a[2])/2,cz=(a[1]+a[3])/2,w=a[2]-a[0],dep=a[3]-a[1];
 function safe(x,z,ww,dd){return !obstacles(r.floor).some(function(c){return x-ww/2<c.box[3]+.08&&x+ww/2>c.box[0]-.08&&z-dd/2<c.box[4]+.08&&z+dd/2>c.box[1]-.08;});}
 if(r.kind==='meeting'){var rows=r.people_assumed>12?3:2;for(var i=0;i<rows;i++){var z=cz+(i-(rows-1)/2)*2.8;if(safe(cx,z,3,3))desk(b,cx,z,true);}b.box('screen',cx,1.75,a[1]+.2,1.8,1.0,.06,0,true);}
 else if(r.function==='Executive'){if(safe(cx,cz-2,1.7,2.4))workstation(b,cx,cz-2,Math.PI);sofa(b,cx,cz+2,2.8,0);cabinet(b,cx,a[1]+.6,Math.min(3,w-1));}
 else if(r.function==='Reception'){b.box('wood',cx,.95,a[1]+1.5,Math.min(3.5,w-1),.12,.75,0,true);sofa(b,cx,cz+1.4,Math.min(3,w-1),0);plantPot(b,a[0]+.8,a[1]+.8);}
 else if(r.kind==='office'){var count=0;for(var z=a[1]+1.8;z<a[3]-1.7;z+=2.6)for(var x=a[0]+1.2;x<a[2]-1.1;x+=2.6){if(count>=r.people_assumed)break;if(safe(x,z,1.5,2.3)){workstation(b,x,z,r.tenant==='A'?0:Math.PI);count++;}}}
 else if(r.kind==='pantry'){cabinet(b,cx,a[1]+.6,w-.8);b.box('metal',a[0]+.8,.94,a[1]+.6,.7,.06,.48,0,true);b.box('metal',a[2]-.7,1.0,a[1]+.65,.65,1.9,.65,0,true);if(safe(cx,cz+1,3,2.8))desk(b,cx,cz+1,true);}
 else if(r.kind==='toilet'){for(var z=a[1]+1.5;z<a[3]-.7;z+=2.5){b.box('wall',a[2]-.85,.45,z,.55,.55,.7,0,true);b.box('wall',a[2]-1.55,1.05,z,.08,2.1,1.5,0,true);}b.box('metal',a[0]+.55,.84,cz,.7,.12,.48,0,true);}
 else if(r.kind==='janitor'){cabinet(b,cx,a[3]-.6,w-.7);b.box('metal',a[0]+.65,.4,a[1]+.9,.65,.8,.6,0,true);b.box('chair',a[2]-.7,.65,cz,.65,1.1,.6,0,true);}
 else if(r.function==='IT'){for(var x=a[0]+.8;x<a[2]-.5;x+=1.3)if(safe(x,a[3]-1.1,.75,1.2))b.box('frame',x,1.05,a[3]-1.1,.65,2.0,.8,0,true);cabinet(b,cx,a[1]+.6,Math.min(3,w-1));}
}

// Office furniture: human scale, shared benches, usable chair bases, joinery and fittings.
window.__SEAT_AUDIT=[];
function seat(b,x,z,angle,target){window.__SEAT_AUDIT.push({room:window.__FURNISH_ROOM,position:[x,z],angle:angle||0,front:[Math.sin(angle||0),-Math.cos(angle||0)],target:target||null});var a=angle||0,c=Math.cos(a),s=Math.sin(a);function p(key,dx,y,dz,w,h,d,rot){b.box(key,x+dx*c-dz*s,y,z+dx*s+dz*c,w,h,d,a+(rot||0),true);}
 p('chair',0,.47,0,.47,.11,.45);p('chair',0,.73,.18,.44,.48,.07);p('frame',0,.29,0,.045,.28,.045);
 for(var k=0;k<5;k++){var t=k*Math.PI*2/5;p('metal',Math.sin(t)*.12,.16,Math.cos(t)*.12,.035,.035,.27,t);p('frame',Math.sin(t)*.24,.095,Math.cos(t)*.24,.065,.10,.045,t);}
 for(var dx of [-.27,.27]){p('frame',dx,.56,.05,.028,.19,.035);p('chair',dx,.66,.01,.06,.035,.28);}p('frame',0,.58,.19,.08,.32,.025);
}
function workstation(b,x,z,angle){var a=angle||0,c=Math.cos(a),s=Math.sin(a);function p(key,dx,y,dz,w,h,d){b.box(key,x+dx*c-dz*s,y,z+dx*s+dz*c,w,h,d,a,true);}
 p('wood',0,.75,0,1.45,.055,.72);p('frame',-.57,.38,0,.045,.71,.60);p('frame',.57,.38,0,.045,.71,.60);p('metal',0,.69,0,1.14,.045,.045);
 p('screen',0,1.03,-.13,.49,.29,.024);p('metal',0,.85,-.13,.055,.18,.045);p('frame',0,.78,-.13,.18,.025,.12);p('frame',-.08,.793,.14,.40,.018,.14);p('chair',.28,.795,.14,.055,.024,.09);p('wall',.57,.79,-.18,.09,.055,.09);
 seat(b,x-Math.sin(a)*.73,z+Math.cos(a)*.73,a,[x,z]);p('wall',-.49,.38,-.03,.28,.57,.55);p('metal',-.49,.48,.26,.14,.015,.018);p('metal',-.49,.25,.26,.14,.015,.018);
}
function sofa(b,x,z,w,angle){var a=angle||0,c=Math.cos(a),s=Math.sin(a);function p(key,dx,y,dz,ww,h,d){b.box(key,x+dx*c-dz*s,y,z+dx*s+dz*c,ww,h,d,a,true);}
 p('frame',0,.18,0,w-.12,.15,.72);p('sofa',0,.72,-.35,w-.12,.64,.15);for(var i=0;i<3;i++)p('sofa',(i-1)*(w-.35)/3,.40,.02,(w-.35)/3-.02,.22,.65);for(var dx of [-w/2+.08,w/2-.08])p('sofa',dx,.51,0,.16,.48,.85);for(var dx of [-w*.4,w*.4])for(var dz of [-.27,.27])p('metal',dx,.085,dz,.045,.12,.045);
}
var beforeR7Furnish=furnishR6;furnishR6=function(b,r){if(!r.r7)return beforeR7Furnish(b,r);var a=r.rect,cx=(a[0]+a[2])/2,cy=(a[1]+a[3])/2;
 if(r.kind==='lobby'){for(var xx of [a[0]+3.2,a[2]-3.2]){sofa(b,xx,cy-2.3,2.8,0);b.box('wood',xx,.40,cy-.9,1.2,.06,.70,0,true);seat(b,xx-.95,cy+.8,Math.PI);seat(b,xx+.95,cy+.8,Math.PI);}plantPot(b,a[0]+.9,a[1]+.9);plantPot(b,a[2]-.9,a[1]+.9);cabinet(b,cx,a[1]+.65,3.6);return;}
 if(r.kind==='meeting'){var n=r.people_assumed,ln=n>=12?5:3.8;var ty=cy-.7;b.box('wood',cx,.76,ty,1.28,.065,ln,0,true);for(var z of [-ln*.38,ln*.38])b.box('frame',cx,.37,ty+z,.75,.72,.075,0,true);for(var i=0;i<(n-2)/2;i++){var yy=ty+(i-((n-2)/2-1)/2)*.86;seat(b,cx-.94,yy,Math.PI/2,[cx,ty]);seat(b,cx+.94,yy,-Math.PI/2,[cx,ty]);}seat(b,cx,ty-ln/2-.6,Math.PI,[cx,ty]);seat(b,cx,ty+ln/2+.6,0,[cx,ty]);b.box('screen',cx,1.70,a[1]+.12,2.0,1.10,.055,0,true);cabinet(b,cx,a[1]+.45,3.2);plantPot(b,a[2]-.75,a[1]+.8);return;}
 beforeR7Furnish(b,r);
 if(r.function==='Open office'){b.box('wood',a[0]+2.3,.40,a[3]-1.6,1.0,.06,.65,0,true);plantPot(b,a[0]+.8,a[3]-.8);b.box('wall',cx,.92,a[1]+3.1,Math.min(8,a[2]-a[0]-2),.32,.045,0,true);}
 if(r.function==='Executive'){b.box('wall',cx,1.6,a[1]+.12,2.0,.7,.04,0,true);plantPot(b,a[0]+.8,a[3]-1.0);}
 if(r.function==='Reception'){b.box('wood',cx,.38,cy+2.3,1.2,.055,.65,0,true);b.box('wall',a[0]+.15,1.65,cy, .04,.6,2.8,0,true);}
 if(r.kind==='pantry'){b.box('frame',a[0]+1.5,1.12,a[1]+.6,.38,.30,.32,0,true);b.box('glass',a[0]+2.2,1.05,a[1]+.6,.08,.18,.08,0,true);}
};

var furnishBeforeR8=furnishR6;furnishR6=function(b,r){window.__FURNISH_ROOM=r.id;furnishBeforeR8(b,r);window.__FURNISH_ROOM=null;};

function waterGeometry(f,parent){for(var svc of ['CHS','CHR']){var verts=[],norm=[],uv=[],index=[],cube=S.cyl(1,1,10),p=cube.attributes.position,n=cube.attributes.normal,u=cube.attributes.uv,idx=cube.index;
 plan.waterPipes.filter(function(e){return e.floor===f&&e.service===svc;}).forEach(function(e){e.points.slice(1).forEach(function(c,i){var a=e.points[i],v=new THREE.Vector3(c[0]-a[0],c[2]-a[2],a[1]-c[1]),len=v.length();if(len<.001)return;var q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize()),center=new THREE.Vector3((a[0]+c[0])/2,(a[2]+c[2])/2,-(a[1]+c[1])/2),off=verts.length/3;
  for(var j=0;j<p.count;j++){var xyz=new THREE.Vector3(p.getX(j)*e.outsideRadius_m,p.getY(j)*len,p.getZ(j)*e.outsideRadius_m).applyQuaternion(q).add(center);verts.push(xyz.x,xyz.y,xyz.z);var nn=new THREE.Vector3(n.getX(j),n.getY(j),n.getZ(j)).applyQuaternion(q);norm.push(nn.x,nn.y,nn.z);uv.push(u.getX(j),u.getY(j));}for(var j=0;j<idx.count;j++)index.push(off+idx.getX(j));
 });});if(verts.length){var geo=new THREE.BoxGeometry(1,1,1);geo.setAttribute('position',new p.constructor(verts,3));geo.setAttribute('normal',new n.constructor(norm,3));geo.setAttribute('uv',new u.constructor(uv,2));geo.setIndex(index);geo.clearGroups();geo.computeBoundingSphere();S.mesh(geo,new THREE.MeshStandardMaterial({color:svc==='CHS'?'#1559d6':'#57c5f5',roughness:.55,metalness:.35,envMapIntensity:.04}),parent);}cube.dispose();}}
function circulationGeometry(f,wb,ib,names){
  // Passenger lifts replace the ordinary stair; two external fire stair towers remain.
  wall(wb,f,28,27,36,27,3.45);wall(wb,f,28,39,36,39);wall(wb,f,28,27,28,39);wall(wb,f,36,27,36,39);
  plan.verticalTransport.lifts.forEach(function(l){var a=l.rect;wall(wb,f,a[0],a[1],a[2],a[1]);wall(wb,f,a[0],a[1],a[0],a[3]);wall(wb,f,a[2],a[1],a[2],a[3]);wall(wb,f,a[0],a[3],a[2],a[3],(a[2]-a[0])/2-.55);ib.box('metal',(a[0]+a[2])/2,1.15,a[3]-.045,1.1,2.25,.035);ib.box('screen',a[2]-.2,1.55,a[3]+.1,.10,.16,.025);flatLabel(names,l.id,(a[0]+a[2])/2,.075,a[3]+.6,2.8);});
  flatLabel(names,'LIFT LOBBY',32,.075,36.4,5);
  plan.verticalTransport.fireStairs.forEach(function(st){var a=st.rect,cx=(a[0]+a[2])/2,cz=(a[1]+a[3])/2,w=a[2]-a[0];ib.box('tile',cx,.025,cz,w,.04,a[3]-a[1]);wall(wb,f,a[0],a[1],a[2],a[1]);wall(wb,f,a[0],a[3],a[2],a[3]);wall(wb,f,a[0],a[1],a[0],a[3],st.id==='FS-E'?.45:undefined);wall(wb,f,a[2],a[1],a[2],a[3],st.id==='FS-W'?.95:undefined);
    var n=Math.ceil(height(f)/.18),half=Math.ceil(n/2),rise=height(f)/n,going=.28;for(var i=0;i<half;i++)ib.box('concrete',cx-.95,rise*(i+.5),a[1]+.5+i*going,1.5,rise,going);ib.box('concrete',cx,height(f)/2-.09,a[1]+.5+half*going,3.8,.18,1.0);for(var i=0;i<n-half;i++)ib.box('concrete',cx+.95,height(f)/2+rise*(i+.5),a[1]+.5+(half-i-1)*going,1.5,rise,going);flatLabel(names,st.id+' / FIRE EXIT',cx,.075,a[3]-.5,3.7);
  });
  if(f>1){for(var xx of [24.5,39.5]){for(var span of [[.5,13.7],[16.8,22.7],[25.3,28.7],[31,39.5]])wall(wb,f,xx,span[0],xx,span[1]);for(var span of [[13.7,16.8,1.0],[22.7,25.3,.75],[28.7,31,.60]])wall(wb,f,xx,span[0],xx,span[1],span[2],true);}flatLabel(names,'COMPANY A / 888.69 m²',12,.075,15.4,9);flatLabel(names,'COMPANY B / 888.69 m²',52,.075,15.4,9);}
  (plan.corridors||[]).filter(function(c){return c.floor===f;}).forEach(function(c){var a=c.rect;ib.box('tile',(a[0]+a[2])/2,.056,(a[1]+a[3])/2,a[2]-a[0],.018,a[3]-a[1]);});
}

// Replace the old plant-room building shell with the coordinated rental-office layout.
S.LAYER.shell.clear();S.LAYER.interiors=new THREE.Group;S.LAYER.ducts=new THREE.Group;S.scene.add(S.LAYER.interiors,S.LAYER.ducts);
for(var child of Array.from(S.LAYER.plant.children))if(!child.userData.eq)S.LAYER.plant.remove(child);
for(var f=0;f<=9;f++){
 var structural=new THREE.Group,facade=new THREE.Group,interior=new THREE.Group,walls=new THREE.Group,names=new THREE.Group,ducts=new THREE.Group,lighting=new THREE.Group,water=new THREE.Group;
 structural.position.y=facade.position.y=interior.position.y=walls.position.y=names.position.y=lighting.position.y=base(f);
 S.LAYER.shell.add(structural,facade);S.LAYER.interiors.add(interior,walls,names,lighting);S.LAYER.ducts.add(ducts,water);
 var beamGroup=new THREE.Group,slabGroup=new THREE.Group;structural.add(beamGroup,slabGroup);storeys[f]={structural:structural,slab:slabGroup,facade:facade,interior:interior,walls:walls,names:names,ducts:ducts,lighting:lighting,water:water,beams:beamGroup};waterGeometry(f,water);
 var sb=batch(structural,f,'structure'),slb=batch(slabGroup,f,'structure'),bb=batch(beamGroup,f,'structure'),fb=batch(facade,f,'envelope'),ib=batch(interior,f,'furniture'),wb=batch(walls,f,'wall'),db=batch(ducts,f,'duct',true),lb=batch(lighting,f,'lights');
 // Explicit slab openings for service risers. Rectangle strips preserve actual holes.
 var holes=f===0?[]:plan.shafts.map(function(s){return s.rect;}).concat(plan.verticalTransport.lifts.map(function(l){return l.rect;}));var xs=[0,64],ys=[0,40];holes.forEach(function(h){xs.push(h[0],h[2]);ys.push(h[1],h[3]);});xs=[...new Set(xs)].sort(function(a,b){return a-b;});ys=[...new Set(ys)].sort(function(a,b){return a-b;});
 for(var i=0;i<xs.length-1;i++)for(var j=0;j<ys.length-1;j++){var x=(xs[i]+xs[i+1])/2,z=(ys[j]+ys[j+1])/2;if(!holes.some(function(h){return x>h[0]&&x<h[2]&&z>h[1]&&z<h[3];}))slb.box('concrete',x,-.14,z,xs[i+1]-xs[i],.28,ys[j+1]-ys[j]);}
 if(f<9){var h=height(f)-.25;plan.columns.filter(function(c){return c.floor===f;}).forEach(function(c){sb.box('concrete',(c.box[0]+c.box[3])/2,h/2,(c.box[1]+c.box[4])/2,.6,h,.6);});plan.beams.filter(function(c){return c.floor===f;}).forEach(function(c){bb.box('concrete',(c.box[0]+c.box[3])/2,(c.box[2]+c.box[5])/2-base(f),(c.box[1]+c.box[4])/2,c.box[3]-c.box[0],.55,c.box[4]-c.box[1]);});
  if(f>0){
   for(var side of [0,40]){fb.box('frame',32,.3,side,64,.6,.13);fb.box('frame',32,h-.2,side,64,.4,.13);for(var xx=0;xx<=64;xx+=2)fb.box('frame',xx,h/2,side,.055,h,.12);
    // Front facade is open in the default sectional perspective, keeping interiors readable.
    if(side===40)fb.box('glass',32,h/2,side,64,h-.65,.02);
   }
   for(var side of [0,64]){fb.box('frame',side,.3,20,.13,.6,40);fb.box('frame',side,h-.2,20,.13,.4,40);for(var zz=0;zz<=40;zz+=2)fb.box('frame',side,h/2,zz,.12,h,.055);if(side===0)fb.box('glass',side,h/2,20,.02,h-.65,40);}
  }
 }
 if(f===0){
  ib.box('tile',32,.025,20,63.8,.035,39.8);wall(wb,0,50,18,63.5,18,7);wall(wb,0,50,26,63.5,26);wall(wb,0,50,18,50,26);wall(wb,0,63.5,18,63.5,26);flatLabel(names,'B1 · CHILLER PLANT',24,.075,22,15);flatLabel(names,'ELECTRICAL',57,.075,25,7);
  for(var xx=3;xx<48;xx+=8){ib.box('SA',xx,.055,18,.06,.02,5);ib.box('SA',xx+2,.055,18,.06,.02,5);}
  for(var xx=6;xx<62;xx+=8)lb.box('luminaire',xx,4.65,18,3.2,.045,.08);
  for(var xx=4;xx<45;xx+=8)lb.box('luminaire',xx,4.65,11,3.2,.045,.08);
 }else if(f<9){
  ib.box('tile',32,.025,20,63.8,.03,39.8);
  rooms.filter(function(r){return r.floor===f;}).forEach(function(r){var a=r.rect,x0=a[0],z0=a[1],x1=a[2],z1=a[3],cx=(x0+x1)/2,cz=(z0+z1)/2;
   ib.box(r.kind==='office'?'carpet':r.kind==='meeting'?'wood':'tile',cx,.049,cz,x1-x0-.12,.026,z1-z0-.12);
   // Every rentable suite has its own corridor door and a glazed private room.
   var doorSide=r.doorSide||(cz<18?'north':'south'),glass=r.kind==='office'||r.kind==='meeting';
   wall(wb,f,x0,z0,x1,z0,doorSide==='south'?(r.doorCenter?r.doorCenter[0]-x0-.55:(x1-x0)/2-.55):undefined,glass);wall(wb,f,x0,z1,x1,z1,doorSide==='north'?(r.doorCenter?r.doorCenter[0]-x0-.55:(x1-x0)/2-.55):undefined,glass);wall(wb,f,x0,z0,x0,z1);wall(wb,f,x1,z0,x1,z1);
   flatLabel(names,r.name,cx,.075,r.id.endsWith('EN3')&&r.kind==='mechanical'?31.5:cz,Math.min(5,x1-x0-.3));
   if(r.kind==='office'&&f>1&&x0<40&&!r.r6){var privateY=cz<18?z1-r.privateDepth_m:z0+r.privateDepth_m;wall(wb,f,x0,privateY,x1,privateY,(x1-x0)/2-.55,true);}
   furnishRoom(ib,r);
   for(var zz=z0+1.2;zz<z1-.5;zz+=3.2)lb.box('luminaire',cx,3.22,zz,Math.min(3.2,x1-x0-.8),.04,.055,0,true);
  });
  plan.shafts.forEach(function(s){var a=s.rect;wall(wb,f,a[0],a[1],a[2],a[1]);wall(wb,f,a[0],a[3],a[2],a[3]);wall(wb,f,a[0],a[1],a[0],a[3]);wall(wb,f,a[2],a[1],a[2],a[3],.8);});
 }else{
  sb.box('concrete',44,1.75,21,8,3.5,12);sb.box('frame',19.6,.9,6,34.5,.2,3);
  for(var xx=0;xx<64;xx+=4)sb.box('frame',xx,.015,20,.012,.02,40);for(var zz=0;zz<40;zz+=4)sb.box('frame',32,.015,zz,64,.02,.012);
  sb.box('frame',32,.45,40,64,.9,.12);sb.box('frame',0,.45,20,.12,.9,40);
 }
 (plan.ductBodies||plan.ducts).filter(function(d){return d.floor===f;}).forEach(function(d){
  d.points.slice(1).forEach(function(c,i){var a=d.points[i],vertical=a[2]!==c[2],len=Math.hypot(c[0]-a[0],c[1]-a[1],c[2]-a[2]),x=(a[0]+c[0])/2,z=(a[1]+c[1])/2,yy=(a[2]+c[2])/2,alongX=a[1]===c[1];
   if(!plan.ductShells)db.box(d.service==='RA'?'returnDuct':'duct',x,yy,z,vertical?d.w:alongX?len:d.w,vertical?len:d.h,vertical?d.h:alongX?d.w:len,0,false);
   if(!vertical)for(var t=1;t<len;t+=2.4){var px=a[0]+(c[0]-a[0])*t/len,pz=a[1]+(c[1]-a[1])*t/len;
    db.box('frame',px,yy,pz,alongX?.025:d.w+.035,d.h+.028,alongX?d.w+.035:.025,0,true);
    // Short support hangers remain below the assumed beam soffit; attachment detail pending.
    var rodStart=yy+d.h/2+.015,rodTop=Math.min(base(f)+height(f)-.835,rodStart+.12);if(rodTop>rodStart)for(var side of [-1,1])db.box('metal',px+(alongX?0:side*(d.w/2+.08)),(rodStart+rodTop)/2,pz+(alongX?side*(d.w/2+.08):0),.014,rodTop-rodStart,.014,0,true);
    if(t===1)db.box(d.service,px,yy+d.h/2+.022,pz,alongX?.2:d.w,.02,alongX?d.w:.2);
   }
  });
  if(f===1&&(d.id.startsWith('OA-to-')||d.id.startsWith('FCU-SA-')||d.id.startsWith('PRIVATE-SA-')||d.id.startsWith('PRIVATE-OA-'))){var p=d.points[d.points.length-1];db.box('metal',p[0],p[2]-.18,p[1],.6,.055,.6,0,true);for(var w of [.46,.33,.2]){db.box('wall',p[0],p[2]-.14,p[1]-w/2,w,.02,.025,0,true);db.box('wall',p[0],p[2]-.14,p[1]+w/2,w,.02,.025,0,true);}db.box('SA',p[0],p[2]-.12,p[1],.12,.02,.12,0,true);}
  if(f===1&&(d.id.startsWith('RA-F')||d.id.startsWith('TE-F')||d.id.startsWith('PRIVATE-RA-'))){var p=d.points[0];db.box('frame',p[0],p[2]-.15,p[1],.5,.035,.5,0,true);for(var z=-.18;z<.2;z+=.06)db.box('metal',p[0],p[2]-.12,p[1]+z,.45,.015,.024,0,true);}
 });
 (plan.diffusers||[]).filter(function(t){return t.floor===f;}).forEach(function(t){var p=t.position,w=t.face_m[0],d=t.face_m[1];if(t.service==='TA'){db.box('metal',p[0],p[2],p[1],w,d,.04,0,true);for(var yy=-d*.4;yy<d*.4;yy+=.04)db.box('frame',p[0],p[2]+yy,p[1]+.025,w*.9,.015,.02,0,true);return;}db.box('metal',p[0],p[2],p[1],w,.045,d,0,true);if(t.service==='SA'||t.service==='OA'){for(var k of [.8,.58,.36]){db.box('wall',p[0],p[2]-.025,p[1]-d*k/2,w*k,.025,.025,0,true);db.box('wall',p[0],p[2]-.025,p[1]+d*k/2,w*k,.025,.025,0,true);db.box('wall',p[0]-w*k/2,p[2]-.025,p[1],.025,.025,d*k,0,true);db.box('wall',p[0]+w*k/2,p[2]-.025,p[1],.025,.025,d*k,0,true);}}else for(var k=-d*.4;k<d*.4;k+=.065)db.box('frame',p[0],p[2]-.03,p[1]+k,w*.85,.025,.02,0,true);});
 // Unmapped tenant FCUs and roof units are design objects, never fabricated LIVE points.
 /* r6: roof design units are drawn by devices79.js (Blender) */[].forEach(function(e){var p=e.position,w=e.size[0],d=e.size[1],h=e.size[2];db.box('metal',p[0],p[2]+h/2,p[1],w,h,d,0,true);db.box('insulated',p[0],p[2]+h*.55,p[1]+d/2+.015,w*.7,h*.6,.025,0,true);db.box('frame',p[0],p[2]-.035,p[1],w+.10,.035,d+.08,0,true);
  if(e.floor===9){for(var x=p[0]-w/2+.5;x<p[0]+w/2;x+=.7){db.box('frame',x,p[2]+h/2,p[1]+d/2+.02,.025,h,.04,0,true);db.box('metal',x+.15,p[2]+h*.55,p[1]+d/2+.05,.04,.28,.035,0,true);}db.box('frame',p[0],p[2]+h+.04,p[1],w+.16,.06,d+.16);for(var z=p[1]-d/2+.12;z<p[1]+d/2;z+=.11)db.box('frame',p[0]+w/2+.02,p[2]+h*.5,z,.04,h*.65,.028);}
 });
 if(f<9)circulationGeometry(f,wb,ib,names);else plan.verticalTransport.fireStairs.forEach(function(st){var a=st.rect;slb.box('concrete',(a[0]+a[2])/2,-.14,(a[1]+a[3])/2,a[2]-a[0],.28,a[3]-a[1]);flatLabel(names,st.id+' ROOF EXIT',(a[0]+a[2])/2,.075,a[3]-.4,3.8);});
 sb.flush();slb.flush();bb.flush();fb.flush();ib.flush();wb.flush();db.flush();lb.flush();
}
(plan.ductShells||[]).forEach(function(s){var geo=new THREE.BoxGeometry(1,1,1),attr=geo.attributes.position.constructor;geo.setIndex(null);geo.clearGroups();geo.setAttribute('position',new attr(new Float32Array(s.positions),3));geo.deleteAttribute('uv');geo.deleteAttribute('normal');geo.computeVertexNormals();geo.computeBoundingSphere();var material=new THREE.MeshStandardMaterial({color:s.service==='RA'?'#a4a9a6':'#b1bfc3',metalness:.12,roughness:.6,transparent:true,opacity:.19,depthWrite:false,side:THREE.DoubleSide});var mesh=S.mesh(geo,material,storeys[s.floor].ducts);mesh.userData.designKind='duct';mesh.userData.service=s.service;mesh.renderOrder=8;});
// Warm lights are deliberately limited; the emissive ceiling strips provide most detail.
for(var f=0;f<=8;f++){for(var xy of [[18,10],[18,33],[55,8],[55,33]]){var light=new THREE.PointLight(0xffe2b5,180,26,2);light.position.set(xy[0],f===0?4.8:3.25,-xy[1]);storeys[f].lighting.add(light);}}
for(var xx of [4,12,20,28,36,44]){var light=new THREE.PointLight(0xd6e9ff,260,15,2);light.position.set(xx,4.5,-10);storeys[0].lighting.add(light);}
for(var id in S.EQ){var u=S.EQ[id];u.mats.forEach(function(m){if(m.isMeshStandardMaterial)m.envMapIntensity=.05;});if(u.e.type==='chiller'){if(u.parts.evap)u.parts.evap.material.color.set('#3f4b4f');if(u.parts.cond)u.parts.cond.material.color.set('#aab4b5');}if(u.e.type==='pump')u.mats.forEach(function(m){if(m.color&&m.color.getHexString()==='345e73')m.color.set('#315e7b');});if(u.e.type==='ahu'){u.mats.forEach(function(m){if(m.color&&m.color.getHexString()==='d2d8d7')m.color.set('#a8b8b1');});for(var side of [-1,1])S.mesh(S.box(.16,.6,.9),mat.duct,u.g,new THREE.Vector3(side*(S.mm(u.e.L)/2+.08),S.mm(u.e.H)*.62,0));}}
for(var id in S.EQ){var u=S.EQ[id];if(u.parts.evap){var insulation=u.parts.evap.material.clone();insulation.color.set('#2c3d42');insulation.metalness=.08;insulation.roughness=.85;u.parts.evap.material=insulation;u.mats.add(insulation);}}
S.svcMat.CHS.color.set('#1559d6');S.svcMat.CHR.color.set('#57c5f5');S.svcMat.CDS.color.set('#efc72f');S.svcMat.CDR.color.set('#ed781c');
for(var key in S.svcMat)S.svcMat[key].envMapIntensity=.035;
var pipeFinishes={CHS:'#1559d6',CHR:'#57c5f5',CDS:'#efc72f',CDR:'#ed781c'};
for(var id in S.PIPE){var p=S.PIPE[id],color=pipeFinishes[p.p.svc];if(color){p.mat.color.set(color);p.mat.envMapIntensity=.05;p.mat.roughness=.48;p.oc=p.mat.color.clone();S.svcMat[p.p.svc+'_band'].color.set(plan.pipeColors[p.p.svc]);}}
for(var id in S.EQ){var u=S.EQ[id];if(u.e.type==='ahu'){S.mesh(S.box(.8,.25,.18),mat.duct,u.g,new THREE.Vector3(0,1.47,S.mm(u.e.W)/2+.08));if(u.e.floor<9){for(var ph of [[-.9,1.5],[-1.3,.9]]){S.mesh(S.cyl(.065,.16,14),mat.blue,u.g,new THREE.Vector3(ph[0],ph[1],-.95),[Math.PI/2,0,0]);S.mesh(S.cyl(.11,.03,16),mat.metal,u.g,new THREE.Vector3(ph[0],ph[1],-1.015),[Math.PI/2,0,0]);}}}}
var controls=document.createElement('div');controls.className='office-controls';controls.innerHTML='<h2>Office / Food court · R3</h2><label><input data-layer="interiors" type="checkbox" checked> Rooms / furniture / lighting</label><label><input data-layer="ducts" type="checkbox" checked> AHU duct / VAV / damper</label><label><input id="officeNames" type="checkbox"> Room names</label><label>Wall cutaway <select id="officeWalls"><option value="0.43">Low 1.25 m</option><option value="1">Full 2.9 m</option></select></label><label>Lighting <select id="officeTheme"><option value="dusk">Dusk · warm light</option><option value="day">Day · real materials</option><option value="night">Night · building section</option></select></label><small>Coordinated concept · B1 plant<br>AHU VAV / hood / MAU points per the r6 layer</small>';
document.querySelector('aside section').appendChild(controls);controls.querySelectorAll('label').forEach(function(l){l.style.display='block';l.style.margin='7px 0';});
controls.insertAdjacentHTML('afterbegin','<label><input id="officeSection" type="checkbox"> Open the ground floor to see B1 (columns / beams kept)</label>');
controls.insertAdjacentHTML('beforeend','<label><input id="officeWater" type="checkbox" checked> CHW piping to AHU / PICV</label>');
controls.insertAdjacentHTML('beforeend','<label><input id="officeBeams" type="checkbox" checked> Show beams</label>');
controls.querySelectorAll('label').forEach(function(l){l.style.display='block';l.style.margin='7px 0';});
// The presentation cut changes visibility only. Audits always check the full geometry.
var frontSection=new THREE.Plane(new THREE.Vector3(0,0,-1),-14);
// Remove the original floating parking marks and lamps from this basement concept.
S.scene.children.forEach(function(o){if(Math.abs(o.position.y+.29)<.002&&o.isMesh)o.visible=false;if(o.position.z===22&&Math.abs(o.position.y+.3)<.002)o.visible=false;});
function applyTheme(){var theme=S.$('officeTheme').value;S.sky.visible=false;S.scene.background=new THREE.Color(theme==='day'?'#bdc9cd':theme==='dusk'?'#233b4b':'#0d2132');S.scene.fog=null;
 S.sun.position.set(45,95,35);S.sun.intensity=theme==='day'?2.5:theme==='dusk'?1.3:.65;S.sun.color.set('#fff4de');S.hemi.intensity=theme==='day'?1.7:theme==='dusk'?1.25:.9;S.hemi.color.set('#d4e0e5');S.hemi.groundColor.set('#8a8070');S.renderer.toneMappingExposure=theme==='day'?1.05:theme==='dusk'?1.15:1.2;
}
var oldEv=S.applyWeather;S.applyWeather=function(i,t){oldEv(i,t);applyTheme();};S.$('officeTheme').addEventListener('change',applyTheme);applyTheme();
S.$('labelsOn').checked=false;S.$('labelsOn').dispatchEvent(new Event('change'));S.LAYER.zones.visible=false;
var legacyLayer=document.querySelector('[data-layer="zones"]');legacyLayer.checked=true;S.LAYER.zones.visible=true;legacyLayer.parentElement.lastChild.textContent=' Room colours · Temperature / RH / CO₂';
S.$('fsel').insertAdjacentHTML('afterbegin','<option value="0">B1 · Chiller plant</option>');
function available(u){return !u.e.slot||S.isInst(u.e.slot,S.M.installed[u.e.slot]);}
function currentFloor(u){return u.e.floor!==undefined?u.e.floor:u.e.type==='ct'?9:0;}
function visibleFloor(f){return S.FSEL==='all'||S.FSEL==='roof'?(S.FSEL==='all'||f===9):S.ISO?f===+S.FSEL:f<=+S.FSEL;}
S.applyFloor=function(){var selected=/^\d+$/.test(S.FSEL),isolate=selected&&S.ISO,low=selected?base(+S.FSEL)-.3:-7,high=selected?base(+S.FSEL)+height(+S.FSEL)-.2:40,planes=isolate?[new THREE.Plane(new THREE.Vector3(0,1,0),-low),new THREE.Plane(new THREE.Vector3(0,-1,0),high)]:null;
 S.LAYER.plant.visible=S.LAYCHK('plant');S.LAYER.piping.visible=S.LAYCHK('piping');S.LAYER.air.visible=S.LAYCHK('air');S.LAYER.interiors.visible=S.LAYCHK('interiors');S.LAYER.ducts.visible=S.LAYCHK('ducts');
 for(var f in storeys){var r=storeys[f],show=visibleFloor(+f);r.structural.visible=r.interior.visible=r.walls.visible=r.lighting.visible=r.ducts.visible=show;r.facade.visible=show&&!isolate;r.names.visible=show&&S.$('officeNames').checked;r.walls.scale.y=isolate?+S.$('officeWalls').value:1;
  r.beams.visible=S.$('officeBeams').checked;
  var lightIndex=0;r.lighting.children.forEach(function(o){if(o.isPointLight){o.visible=isolate||+f===0||lightIndex===0||lightIndex===3;lightIndex++;}});
  r.water.visible=show&&S.$('officeWater').checked;['structural','facade','interior','walls','lighting','ducts','water'].forEach(function(k){r[k].traverse(function(m){if(m.isMesh&&m.material)m.material.clippingPlanes=null;});});
  // Only open the ground-floor slab/finish. Columns, beams and upper floors remain continuous.
  if(+f===1&&S.FSEL==='all'&&S.$('officeSection').checked){r.slab.traverse(function(m){if(m.isMesh)m.material.clippingPlanes=[frontSection];});r.interior.children.forEach(function(m){if(m.isMesh&&m.material.color.getHexString()===mat.tile.color.getHexString())m.material.clippingPlanes=[frontSection];});}
  if(+f===9&&isolate){r.ducts.visible=true;r.ducts.traverse(function(m){if(m.isMesh&&m.material)m.material.clippingPlanes=planes;});}
 }
 for(var id in S.EQ){var u=S.EQ[id];u.g.visible=visibleFloor(currentFloor(u))&&(available(u)||S.$('showSpare').checked);if(S.LBL[id])S.LBL[id].dataset.hidden=u.g.visible&&u.g.parent.visible?'':'1';}
 S.renderer.localClippingEnabled=true;
 for(var id in S.PIPE){var p=S.PIPE[id],ys=p.p.pts.map(function(a){return S.mm(a[2]);}),ok=!isolate||(Math.min(...ys)<=high&&Math.max(...ys)>=low);p.g.visible=ok&&(!p.ghost||S.$('showSpare').checked)&&(S.FSEL!=='roof'||Math.max(...ys)>34.8);p.g.traverse(function(m){if(m.isMesh&&m.material)m.material.clippingPlanes=planes;});}
 for(var key in S.ZONE)S.ZONE[key].g.visible=false;
 S.apron.visible=S.ground.visible=false;S.trees.forEach(function(g){g.visible=false;});
 if(S.devicesFloor)S.devicesFloor(visibleFloor);   // r6: Blender field devices (devices79.js) follow the same floor filter
};
updateSpareVisibility=function(){S.applyFloor();};
function focus(f){S.FSEL=f;S.$('fsel').value=f;S.ISO=/^\d+$/.test(f);S.$('fiso').checked=S.ISO;S.LAYER.shell.visible=true;document.querySelector('[data-layer="shell"]').checked=true;S.applyFloor();var b=/^\d+$/.test(f)?base(+f):f==='roof'?34.9:10;
 if(f==='all')S.flyTo([99,37,79],[32,12,-20]);else if(f==='0')S.flyTo([94,39,49],[32,-3,-17]);else S.flyTo([93,b+53,47],[35,b+1.3,-20]);
}
S.$('fsel').onchange=function(e){focus(e.target.value);};S.$('fiso').onchange=function(){S.ISO=S.$('fiso').checked;S.applyFloor();};controls.querySelectorAll('input,select').forEach(function(c){c.addEventListener('change',S.applyFloor);});
document.querySelectorAll('[data-view]').forEach(function(b){b.onclick=function(){var v=b.dataset.view;S.$('officeBeams').checked=v!=='plant';focus(v==='plant'||v==='pumps'||v==='room'?'0':v==='roof'?'roof':v==='floor'?'3':'all');if(v==='plant')S.flyTo([24,8,-31],[9,-4.7,-11]);if(v==='pumps')S.flyTo([78,9,8],[56,-5,-7]);if(v==='room')S.flyTo([60,2,30],[32,-4,-11]);};});
document.querySelectorAll('[data-view]').forEach(function(b){b.addEventListener('click',function(){S.LAYER.shell.visible=true;document.querySelector('[data-layer="shell"]').checked=true;S.applyFloor();});});
addEventListener('DOMContentLoaded',function(){S.$('navHome').onclick=function(){focus('all');};S.$('navIn').onclick=function(){S.zoomBy(.72);};S.$('navOut').onclick=function(){S.zoomBy(1/.72);};[['navUp',1],['navDn',-1]].forEach(function(p){S.$(p[0]).onclick=function(){focus(String(Math.max(0,Math.min(8,(+S.FSEL||0)+p[1]))));};});});
document.querySelector('header h1').textContent='ALT Office · Lobby / Food court / B1 plant';document.querySelector('header .sub').textContent='Lobby + food court / 7 rental office floors / 119 suites';
document.querySelector('.material-note').textContent='EIT / ASHRAE design basis · sizing and structure still to be confirmed';
// R4: separate room footprints and coordinated, explicitly unbound MEP hardware.
S.LAYER.zones.clear();
var roomCells=[],roomGroups={},deviceGroups={},vavGroups={},hardwareBounds=[];
var palette=['#174ea6','#087f99','#21945c','#b59812','#c05b12','#b51d32'];
function roomColor(value,oos,key){
 if(oos||typeof value!=='number'||!isFinite(value))return new THREE.Color('#455564');
 var scale=S.MRANGE[key],u=Math.max(0,Math.min(1,(value-scale[0])/(scale[1]-scale[0])))*(palette.length-1),i=Math.floor(u);
 return new THREE.Color(palette[i]).lerp(new THREE.Color(palette[Math.min(i+1,palette.length-1)]),u-i);
}
rooms.forEach(function(r){
 var group=roomGroups[r.floor];if(!group){group=roomGroups[r.floor]=new THREE.Group;S.LAYER.zones.add(group);}
 var src=r.legacyZone&&S.ZONE[r.legacyZone]?S.ZONE[r.legacyZone].z:null;
 // A revised ground-floor room cannot silently inherit the former office/meeting sensor.
 // Only the explicit legacyZone mapping in the design registry is used for color.
 var rects=[(r.heatmapRect||r.rect).slice()];
 if(r.kind==='mechanical'&&r.id.endsWith('EN3'))rects[0][3]=32.4; // heatmap on accessible service apron, not on riser slab voids
 if(r.floor>1&&r.kind==='office'&&r.rect[0]<40&&!r.r6){var a=r.rect,p=(a[1]+a[3])/2<18?a[3]-r.privateDepth_m:a[1]+r.privateDepth_m;rects=[[a[0],a[1],a[2],p-.08],[a[0],p+.08,a[2],a[3]]];}
 rects.forEach(function(a,i){
  var bounds=[a[0]+.13,a[1]+.13,a[2]-.13,a[3]-.13],w=bounds[2]-bounds[0],d=bounds[3]-bounds[1];
  var material=new THREE.MeshBasicMaterial({color:'#455564',transparent:true,opacity:.82,depthWrite:false,toneMapped:false,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1});
  var mesh=S.mesh(new THREE.BoxGeometry(w,.018,d),material,group,new THREE.Vector3((bounds[0]+bounds[2])/2,base(r.floor)+.087,-(bounds[1]+bounds[3])/2));mesh.castShadow=mesh.receiveShadow=false;
  var cell={id:r.id+(rects.length>1?'-'+(i+1):''),room:r,source:src,rect:bounds,mesh:mesh,material:material,value:null,state:'unmapped'};
  mesh.userData.roomCell=cell.id;roomCells.push(cell);
  // Visible gaps follow partitions; the fine border remains legible at equal temperatures.
  for(var b of [[(bounds[0]+bounds[2])/2,bounds[1],w,.035],[(bounds[0]+bounds[2])/2,bounds[3],w,.035],[bounds[0],(bounds[1]+bounds[3])/2,.035,d],[bounds[2],(bounds[1]+bounds[3])/2,.035,d]]){
   var edge=S.mesh(new THREE.BoxGeometry(b[2],.012,b[3]),new THREE.MeshBasicMaterial({color:'#c6d5d5',transparent:true,opacity:.75,depthWrite:false,toneMapped:false}),group,new THREE.Vector3(b[0],base(r.floor)+.10,-b[1]));edge.castShadow=false;
  }
 });
});
controls.insertAdjacentHTML('beforeend','<label><input id="officeInstruments" type="checkbox" checked> Valves / TT / PT / FM / BTU</label><label><input id="officeVAV" type="checkbox" checked> VAV / airflow pickup / actuator</label><label><input id="officeDeviceTags" type="checkbox"> Device tags</label><small>Room colours: legacy aggregates by mapping<br>grey = no mapping / no value / OOS<br>Devices show LIVE values only when bound to a station point</small>');
controls.querySelectorAll('label').forEach(function(l){l.style.display='block';l.style.margin='7px 0';});
controls.querySelector('h2').textContent='Office / Food court · R4';
var finish={body:new THREE.MeshStandardMaterial({color:'#525d60',metalness:.7,roughness:.4,envMapIntensity:.04}),flange:new THREE.MeshStandardMaterial({color:'#89979c',metalness:.75,roughness:.38,envMapIntensity:.04}),brass:new THREE.MeshStandardMaterial({color:'#8f8055',metalness:.55,roughness:.5,envMapIntensity:.04}),actuator:new THREE.MeshStandardMaterial({color:'#bb692d',roughness:.65}),screen:new THREE.MeshBasicMaterial({color:'#273f46',toneMapped:false}),wire:new THREE.MeshStandardMaterial({color:'#354b51',roughness:.7})};
function hwMesh(geo,material,parent,p,q){var o=S.mesh(geo,material,parent,p);if(q)o.quaternion.copy(q);return o;}
function coilHardware(d){
 var parent=deviceGroups[d.floor];if(!parent){parent=deviceGroups[d.floor]=new THREE.Group;S.LAYER.piping.add(parent);}
 var g=new THREE.Group;parent.add(g);g.position.set(d.position[0],d.position[2],-d.position[1]);g.userData.instrument=d.id;g.userData.relatedEquipment=d.equipment;
 var axis=new THREE.Vector3(d.direction[0],d.direction[2],-d.direction[1]).normalize(),q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),axis),r=Math.min(.16,Math.max(.025,d.radius));
 var radial=Math.abs(axis.y)>.9?new THREE.Vector3(1,0,0):new THREE.Vector3(0,1,0),stem=radial.clone().multiplyScalar(r+.075),sq=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),radial);
 if(d.kind==='MBFV'||d.kind==='PICV'){
  for(var side of [-1,1])hwMesh(S.cyl(r*1.5,.024,14),finish.flange,g,axis.clone().multiplyScalar(side*.065),q);
  hwMesh(S.cyl(r*1.25,.10,14),d.kind==='PICV'?finish.brass:finish.body,g,new THREE.Vector3(),q);
  hwMesh(S.cyl(.014,.15,10),finish.flange,g,stem,sq);
  hwMesh(new THREE.BoxGeometry(d.kind==='PICV'?.12:.16,.10,.12),finish.actuator,g,radial.clone().multiplyScalar(r+.17));
  if(d.kind==='PICV')for(var side of [-1,1])hwMesh(S.cyl(.012,.07,8),finish.brass,g,axis.clone().multiplyScalar(side*.045).add(radial.clone().multiplyScalar(r+.055)),sq);
 }else if(d.kind==='TT'||d.kind==='PT'){
  hwMesh(S.cyl(.01,r+.11,8),finish.flange,g,radial.clone().multiplyScalar((r+.11)/2),sq);
  hwMesh(d.kind==='TT'?S.cyl(.035,.06,10):new THREE.BoxGeometry(.075,.07,.055),finish.body,g,radial.clone().multiplyScalar(r+.12),d.kind==='TT'?sq:null);
 }else if(d.kind==='FM'){
  for(var side of [-1,1]){var c=axis.clone().multiplyScalar(side*.11).add(radial.clone().multiplyScalar(r+.015));hwMesh(new THREE.BoxGeometry(.075,.065,.06),finish.body,g,c);hwMesh(new THREE.BoxGeometry(.09,.015,.085),finish.actuator,g,c.clone().add(radial.clone().multiplyScalar(.035)));}
 }else if(d.kind==='BTU'){
  var c=radial.clone().multiplyScalar(r+.18);hwMesh(new THREE.BoxGeometry(.20,.14,.10),finish.flange,g,c);hwMesh(new THREE.PlaneGeometry(.14,.06),finish.screen,g,c.clone().add(new THREE.Vector3(0,0,.051)));
 }
 g.updateWorldMatrix(true,true);var bound=new THREE.Box3().setFromObject(g);hardwareBounds.push({id:d.id,kind:d.kind,floor:d.floor,pipe:d.pipe,equipment:d.equipment,box:[bound.min.x,-bound.max.z,bound.min.y,bound.max.x,-bound.min.z,bound.max.y]});
 var tag=S.textSprite(d.kind,28,'#eedbb8','rgba(24,38,44,.9)');tag.position.copy(g.position).add(new THREE.Vector3(0,.42,0));tag.scale.set(1.1,.48,1);tag.userData.hardwareTag=true;tag.userData.relatedEquipment=d.equipment;parent.add(tag);
}
// r6: instruments are drawn by devices79.js (Blender models with station bindings), not by coilHardware
// plan.instruments.forEach(coilHardware);
plan.airTerminals.forEach(function(d){
 var parent=vavGroups[d.floor];if(!parent){parent=vavGroups[d.floor]=new THREE.Group;S.LAYER.ducts.add(parent);}
 var g=new THREE.Group;parent.add(g);g.position.set(d.position[0],d.position[2],-d.position[1]);g.userData.instrument=d.id;
 var alongX=d.direction[0]!==0,w=alongX?d.length:d.w,depth=alongX?d.w:d.length;
 // Inline casing wraps the branch. Actuator is below the casing, outside beam soffits.
 hwMesh(new THREE.BoxGeometry(w,d.h+.035,depth),mat.duct,g,new THREE.Vector3());
 for(var side of [-1,1])hwMesh(new THREE.BoxGeometry(alongX?.018:d.w+.025,d.h+.06,alongX?d.w+.025:.018),finish.flange,g,new THREE.Vector3(alongX?side*d.length/2:0,0,alongX?0:side*d.length/2));
 hwMesh(new THREE.BoxGeometry(.14,.09,.10),finish.actuator,g,new THREE.Vector3(0,-d.h/2-.07,0));
 hwMesh(S.cyl(.009,d.w*.75,8),finish.flange,g,new THREE.Vector3(alongX?-.12:0,0,alongX?0:-.12),new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),alongX?new THREE.Vector3(0,0,1):new THREE.Vector3(1,0,0)));
 hwMesh(new THREE.BoxGeometry(.065,.05,.04),finish.body,g,new THREE.Vector3(.12,-d.h/2-.045,0));
 g.updateWorldMatrix(true,true);var b=new THREE.Box3().setFromObject(g);hardwareBounds.push({id:d.id,kind:'VAV',floor:d.floor,duct:d.duct,box:[b.min.x,-b.max.z,b.min.y,b.max.x,-b.min.z,b.max.y]});
 var tag=S.textSprite('VAV',28,'#eedbb8','rgba(24,38,44,.9)');tag.position.copy(g.position).add(new THREE.Vector3(0,.36,0));tag.scale.set(1.1,.48,1);tag.userData.hardwareTag=true;parent.add(tag);
});
var lastRoomUpdate=0,oldRoomBv=S.updateZones;
S.updateZones=function(dt){oldRoomBv(dt);var time=performance.now();if(time-lastRoomUpdate<300)return;lastRoomUpdate=time;
 roomCells.forEach(function(c){var src=c.source,v=src?S.V[src[S.METRIC]]:null,oos=src?!!S.V[src.oos]:true;c.value=typeof v==='number'&&isFinite(v)?v:null;c.state=!src?'unmapped':oos?'oos':c.value===null?'missing':'aggregate';c.material.color.copy(roomColor(v,oos,S.METRIC));c.material.opacity=c.state==='aggregate'?.82:.72;});
 var legend=S.$('zlegend');if(legend){var range=S.MRANGE[S.METRIC];legend.innerHTML='<span>'+range[0]+' '+range[2]+'</span><i style="background:linear-gradient(90deg,'+palette.join(',')+')"></i><span>'+range[1]+' '+range[2]+'</span>';}
};
var basePrR4=S.applyFloor;S.applyFloor=function(){basePrR4();S.LAYER.zones.visible=S.LAYCHK('zones');
 S.VALVE.forEach(function(v){if(v.v.designReplacement)v.g.visible=false;});
 Object.keys(roomGroups).forEach(function(f){roomGroups[f].visible=visibleFloor(+f);});
 Object.keys(deviceGroups).forEach(function(f){deviceGroups[f].visible=visibleFloor(+f)&&S.$('officeInstruments').checked;});
 Object.keys(vavGroups).forEach(function(f){vavGroups[f].visible=visibleFloor(+f)&&S.$('officeVAV').checked;});
 [deviceGroups,vavGroups].forEach(function(groups){Object.values(groups).forEach(function(g){g.children.forEach(function(o){var u=S.EQ[o.userData.relatedEquipment],show=!u||available(u)||S.$('showSpare').checked;o.visible=show&&(!o.userData.hardwareTag||S.$('officeDeviceTags').checked);});});});
};
['officeInstruments','officeVAV','officeDeviceTags'].forEach(function(id){S.$(id).addEventListener('change',S.applyFloor);});
var zoneRow=document.querySelector('.zrow');if(zoneRow)zoneRow.style.display='';
function openRoomCell(id){var cell=roomCells.find(function(c){return c.id===id;});if(!cell)return;var src=cell.source,metric=S.MRANGE[S.METRIC][2];
 S.$('info').innerHTML='<h3>'+cell.id+' · '+cell.room.name+'</h3><table><tr><td>Floor</td><td>'+cell.room.floor+'</td></tr><tr><td>Displayed value</td><td>'+(cell.value===null?'—':cell.value.toFixed(S.METRIC==='t'?1:0)+' '+metric)+'</td></tr><tr><td>Data source</td><td>'+(src?src.code+' · '+src.name:'no mapping')+'</td></tr><tr><td>Point</td><td>'+(src?src[S.METRIC]:'—')+'</td></tr></table><p>'+(src?'Legacy zone aggregate shared by several rooms (no dedicated room sensor)':'New design room: no dedicated room point')+'</p>';S.$('info').className='open';
}
S.renderer.domElement.addEventListener('dblclick',function(e){if(!S.LAYER.zones.visible)return;var rect=S.renderer.domElement.getBoundingClientRect();S.mp.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);S.ray.setFromCamera(S.mp,S.camera);
 var hit=S.ray.intersectObjects(roomCells.filter(function(c){return roomGroups[c.room.floor].visible;}).map(function(c){return c.mesh;}),false)[0];if(!hit)return;
 var eqHit=S.ray.intersectObjects([...S.LAYER.plant.children,...S.LAYER.air.children],true).find(function(h){var p=h.object;while(p&&!p.userData.eq)p=p.parent;return p&&p.visible&&h.distance<hit.distance;});if(eqHit)return;
 e.stopImmediatePropagation();openRoomCell(hit.object.userData.roomCell);
},true);
window.__R4={roomCells:roomCells,hardwareBounds:hardwareBounds,openRoom:openRoomCell,existingValveBounds:function(){return S.VALVE.filter(function(v){return !v.v.designReplacement;}).map(function(v){v.g.updateWorldMatrix(true,true);var b=new THREE.Box3().setFromObject(v.g);return {kind:v.v.kind,pipe:v.v.pipe,box:[b.min.x,-b.max.z,b.min.y,b.max.x,-b.min.z,b.max.y]};});},inspect:function(){return {revision:plan.revision,roomCells:roomCells.length,mappedCells:roomCells.filter(function(c){return !!c.source;}).length,
 visibleCells:roomCells.filter(function(c){return S.LAYER.zones.visible&&roomGroups[c.room.floor].visible;}).length,instruments:plan.instruments.length,VAVs:plan.airTerminals.length,zoneLayer:S.LAYER.zones.visible,
 upperColumnsClipped:storeys[1].structural.children.filter(function(o){return o.isMesh&&o.material.clippingPlanes&&o.material.clippingPlanes.length;}).length,
 visibleDeviceEquipment:Object.values(deviceGroups).filter(function(g){return g.visible;}).flatMap(function(g){return g.children.filter(function(o){return o.userData.instrument&&o.visible;}).map(function(o){return o.userData.relatedEquipment;});}),
 continuousColumnStacks:plan.columns.length,section:S.$('officeSection').checked};}};

// Dedicated rental-room sensors and whole-floor metering; new points are never fabricated LIVE.
var roomValues={},floorMeterValues={},sensorGroups={},meterGroups={},r5Bounds=[],demoFreeze=false,activeRoom=null,activeMeter=null;
plan.roomSensors.forEach(function(s,i){
 var c=roomCells.find(function(c){return c.id===s.cell;});if(c){c.source=null;c.sensor=s;}
 roomValues[s.cell]={t:null,h:null,c:null,o:null,quality:'unbound'};
 var parent=sensorGroups[s.floor];if(!parent){parent=sensorGroups[s.floor]=new THREE.Group;S.LAYER.interiors.add(parent);}
 var g=new THREE.Group;parent.add(g);g.position.set(s.position[0],s.position[2],-s.position[1]);g.userData.sensor=s.id;
 hwMesh(new THREE.BoxGeometry(.115,.135,.040),mat.wall,g,new THREE.Vector3());hwMesh(new THREE.PlaneGeometry(.078,.043),finish.screen,g,new THREE.Vector3(0,.014,.021));
 g.rotation.y=Math.PI/2;
 var tag=S.textSprite('RS',22,'#e4edf1','rgba(18,43,60,.88)');tag.position.copy(g.position).add(new THREE.Vector3(0,.21,0));tag.scale.set(.56,.28,1);tag.userData.hardwareTag=true;parent.add(tag);
 g.updateWorldMatrix(true,true);var b=new THREE.Box3().setFromObject(g);r5Bounds.push({id:s.id,kind:'ROOM-SENSOR',floor:s.floor,box:[b.min.x,-b.max.z,b.min.y,b.max.x,-b.min.z,b.max.y]});
});
function meterCabinet(m,kind,pos){var parent=meterGroups[m.floor];if(!parent){parent=meterGroups[m.floor]=new THREE.Group;S.LAYER.interiors.add(parent);}var g=new THREE.Group;parent.add(g);g.position.set(pos[0],pos[2],-pos[1]);g.userData.meter=kind==='PM'?m.powerMeter:m.btuMeter;
 hwMesh(new THREE.BoxGeometry(.32,.36,.10),mat.wall,g,new THREE.Vector3());hwMesh(new THREE.PlaneGeometry(.23,.095),finish.screen,g,new THREE.Vector3(0,.06,.051));hwMesh(new THREE.BoxGeometry(.045,.035,.018),finish.actuator,g,new THREE.Vector3(.06,-.08,.06));
 var tag=S.textSprite(g.userData.meter,26,'#e4edf1','rgba(18,43,60,.90)');tag.position.copy(g.position).add(new THREE.Vector3(0,.39,0));tag.scale.set(1.5,.40,1);parent.add(tag);
 g.updateWorldMatrix(true,true);var b=new THREE.Box3().setFromObject(g);r5Bounds.push({id:g.userData.meter,kind:kind,floor:m.floor,box:[b.min.x,-b.max.z,b.min.y,b.max.x,-b.min.z,b.max.y]});
}
plan.floorMeters.forEach(function(m){meterCabinet(m,'PM',m.powerPosition);meterCabinet(m,'BTU',m.position);});
controls.querySelector('h2').textContent='Rental office / Food court · R5';
controls.querySelectorAll('small').forEach(function(s){if(s.textContent.includes('aggregate'))s.remove();});
controls.insertAdjacentHTML('beforeend','<label><input id="officeRoomSensors" type="checkbox" checked> Room sensors</label><label><input id="officeFloorMeters" type="checkbox" checked> Floor power / BTU meters</label><label><input id="rentalDemo" type="checkbox" '+(S.DEMO?'checked':'')+'> Simulate sensors / meters (DEMO)</label><small id="rentalSource"></small><div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;font-size:11px"><span style="color:#1559d6">■ CHWS → load</span><span style="color:#57c5f5">■ CHWR → chiller</span><span style="color:#ed781c">■ CDR → tower</span><span style="color:#b29313">■ CDS → chiller</span></div><details><summary>Floor meters / billing</summary><div id="floorBillingState"></div><a href="ALT_V79_FloorBilling.html" target="_blank" style="display:block;margin-top:8px">Read meters / calculate billing</a></details>');
controls.querySelectorAll('label').forEach(function(l){l.style.display='block';l.style.margin='8px 0';});S.$('rentalSource').style.display='block';S.$('rentalSource').style.lineHeight='1.6';
document.querySelector('header h1').textContent='ALT Rental Office · B1 plant · R5';
document.querySelector('header .sub').textContent='119 suites / 305 dedicated room sensors / 8 floor power + BTU meters';
var priorR5pr=S.applyFloor;S.applyFloor=function(){priorR5pr();[sensorGroups,meterGroups].forEach(function(gs,j){Object.keys(gs).forEach(function(f){gs[f].visible=visibleFloor(+f)&&S.$(j?'officeFloorMeters':'officeRoomSensors').checked;gs[f].children.forEach(function(o){if(o.userData.hardwareTag)o.visible=S.$('officeDeviceTags').checked;});});});};
['officeRoomSensors','officeFloorMeters','rentalDemo'].forEach(function(id){S.$(id).addEventListener('change',function(){S.applyFloor();updateRental();});});
function isRentalDemo(){return S.$('rentalDemo').checked;}
function updateRental(){var demo=isRentalDemo(),sec=performance.now()/1000;
 if(!demoFreeze)plan.roomSensors.forEach(function(s,i){var h=0;for(var ch of s.cell)h=(h*31+ch.charCodeAt(0))>>>0;var phase=(h%1000)/83,val=roomValues[s.cell];
  val.t=demo?23+(h%50)/10+.25*Math.sin(sec/45+phase):null;val.h=demo?47+(h%180)/10+Math.sin(sec/55+phase)*2:null;
  val.c=demo&&s.metrics.includes('CO2_ppm')?450+(h%530)+20*Math.sin(sec/60+phase):null;val.o=demo&&s.metrics.includes('Occupancy')?(h%3!==0):null;val.quality=demo?'demo':'unbound';
 });
 roomCells.forEach(function(c){var v=roomValues[c.id],value=v[S.METRIC];c.value=typeof value==='number'&&isFinite(value)?value:null;c.state=v.quality==='demo'?(c.value===null?'not-applicable':'dedicated-demo'):v.quality;
  c.material.color.copy(roomColor(c.value,v.quality!=='demo',S.METRIC));c.material.opacity=c.state==='dedicated-demo'?.86:.72;
 });
 S.$('rentalSource').textContent=demo?'DEMO · every room sensor is independent; floor meters are simulated':'LIVE · station sensors / meters; grey and — = no value received';
 plan.floorMeters.forEach(function(m){var f=m.floor,pbase=48+f*7,tbase=f===1?260:155+f*9,power=pbase+3*Math.sin(sec/45+f),thermal=tbase+4*Math.sin(sec/50+f),supply=6.7,ret=12.2;
  floorMeterValues[f]={quality:demo?'demo':'unbound',power_kW:demo?power:null,electric_kWh:demo?10000*f+(pbase*sec+135*(Math.cos(f)-Math.cos(sec/45+f)))/3600:null,thermal_kW:demo?thermal:null,thermal_kWh:demo?20000*f+(tbase*sec+200*(Math.cos(f)-Math.cos(sec/50+f)))/3600:null,supply_C:demo?supply:null,return_C:demo?ret:null,flow_m3h:demo?thermal/(1.163*(ret-supply)):null};
 });
 var floor=/^\d+$/.test(S.FSEL)?+S.FSEL:2,m=plan.floorMeters.find(function(m){return m.floor===floor;});
 if(m){var v=floorMeterValues[floor];S.$('floorBillingState').innerHTML='<p>F'+String(floor).padStart(2,'0')+' · '+m.mode+'</p><p>'+m.powerMeter+' / '+m.btuMeter+'</p><p>'+(demo?v.power_kW.toFixed(1)+' kW / '+v.thermal_kW.toFixed(1)+' kW_th<br>'+v.electric_kWh.toFixed(1)+' kWh_e / '+v.thermal_kWh.toFixed(1)+' kWh_th<br>DEMO · values restart on reload':'— / LIVE unbound')+'</p><p>Billing uses verified opening / closing readings</p>';}else S.$('floorBillingState').textContent='B1 / roof are common areas outside the rental-floor billing boundary';
 if(S.$('info').className==='open'){if(activeRoom)openRoomCell(activeRoom);else if(activeMeter)openFloorMeter(activeMeter);}
}
var priorR5Bv=S.updateZones;S.updateZones=function(t){priorR5Bv(t);updateRental();};
openRoomCell=function(id){var c=roomCells.find(function(c){return c.id===id;});if(!c)return;var v=roomValues[id],s=c.sensor;
 activeRoom=id;activeMeter=null;
 S.$('info').innerHTML='<h3>'+s.cell+' · '+s.function+'</h3><table><tr><td>Sensor</td><td>'+s.id+'</td></tr><tr><td>Temperature</td><td>'+(v.t===null?'—':v.t.toFixed(1)+' °C')+'</td></tr><tr><td>RH</td><td>'+(v.h===null?'—':v.h.toFixed(0)+' %')+'</td></tr><tr><td>CO₂</td><td>'+(v.c===null?'—':v.c.toFixed(0)+' ppm')+'</td></tr><tr><td>Occupancy</td><td>'+(v.o===null?'—':v.o?'Occupied':'Unoccupied')+'</td></tr></table><p>'+ (v.quality==='demo'?'DEMO · simulated per-room sensor values, not the legacy aggregates':'LIVE · room sensor points')+'</p><p>installed '+s.height_m+' m AFF · '+s.function+'</p>';S.$('info').className='open';
};
function openFloorMeter(id){var m=plan.floorMeters.find(function(m){return m.powerMeter===id||m.btuMeter===id;});if(!m)return;activeMeter=id;activeRoom=null;var v=floorMeterValues[m.floor],power=id===m.powerMeter,good=v.quality==='demo';
 function fmt(key,unit){return v[key]===null?'—':v[key].toFixed(2)+' '+unit;}
 S.$('info').innerHTML='<h3>'+id+' · F'+String(m.floor).padStart(2,'0')+'</h3><table><tr><td>Power</td><td>'+fmt(power?'power_kW':'thermal_kW',power?'kW':'kW_th')+'</td></tr><tr><td>Energy</td><td>'+fmt(power?'electric_kWh':'thermal_kWh',power?'kWh_e':'kWh_th')+'</td></tr>'+(power?'':'<tr><td>Flow</td><td>'+fmt('flow_m3h','m³/h')+'</td></tr><tr><td>TT-S / TT-R</td><td>'+fmt('supply_C','°C')+' / '+fmt('return_C','°C')+'</td></tr>')+'</table><p>'+(good?'DEMO · simulated values restart on reload (display test only)':'LIVE · floor meter points')+'</p><p>'+m.mode+' · includes the floor AHU / electrical</p><a href="ALT_V79_FloorBilling.html" target="_blank">Open floor billing</a>';S.$('info').className='open';
}
S.renderer.domElement.addEventListener('click',function(e){var rect=S.renderer.domElement.getBoundingClientRect();S.mp.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);S.ray.setFromCamera(S.mp,S.camera);var groups=[...Object.values(sensorGroups),...Object.values(meterGroups)].filter(function(g){return g.visible;});var hit=S.ray.intersectObjects(groups,true).find(function(h){var p=h.object;while(p&&!p.userData.sensor&&!p.userData.meter)p=p.parent;return p;});if(!hit)return;var p=hit.object;while(p&&!p.userData.sensor&&!p.userData.meter)p=p.parent;if(p.userData.meter)openFloorMeter(p.userData.meter);else{var s=plan.roomSensors.find(function(s){return s.id===p.userData.sensor;});openRoomCell(s.cell);}e.stopImmediatePropagation();},true);
window.__R4.openRoom=function(id){openRoomCell(id);};
// Match pipe shells, identification bands and water shader to the same four-service palette.
for(var id in S.PIPE){var p=S.PIPE[id],col=plan.pipeColors[p.p.svc];if(col){p.mat.color.set(col);p.oc=p.mat.color.clone();if(p.wm&&p.wm.uniforms){for(var key in p.wm.uniforms){var u=p.wm.uniforms[key];if(u.value&&u.value.isColor)u.value.set(col);}}}}
window.__R5={roomValues:roomValues,floorMeterValues:floorMeterValues,bounds:r5Bounds,setDemo:function(v){S.$('rentalDemo').checked=v;updateRental();},freeze:function(v){demoFreeze=v;},update:updateRental,openRoom:openRoomCell,openMeter:openFloorMeter,inspect:function(){return {revision:plan.revision,sensors:plan.roomSensors.length,roomCells:roomCells.length,powerMeters:plan.floorMeters.length,btuMeters:plan.floorMeters.length,demo:isRentalDemo(),sensorPointsBound:0,meterPointsBound:0,layouts:[...new Set(rooms.filter(r=>r.kind==='office'&&r.floor>1).map(r=>r.function))],colors:plan.pipeColors};}};
S.applyFloor();updateRental();window.__DESIGN.version='OFFICE-B1-R5';

// Room readings follow actual air terminals; remove the former four aggregate labels.
for(var k in S.ZONE){var old=S.ZONE[k];old.g.visible=false;if(old.sp){old.sp.visible=false;if(old.sp.parent)old.sp.parent.remove(old.sp);}}
palette=['#0639b0','#006b96','#087735','#a28100','#b04400','#b00927'];
controls.querySelector('h2').textContent='Two rental companies / Room HVAC · R7';
document.querySelector('header h1').textContent='ALT Rental Office · Two companies / floor · R7';
document.querySelector('header .sub').textContent='F02–F08 · Company A left / Company B right · room sensors / motorized dampers';
S.$('labelsOn').checked=false;S.$('labelsOn').closest('label').style.display='none';
controls.insertAdjacentHTML('beforeend','<label><input id="roomReadingsR6" type="checkbox" checked> room temperature figures where a grille exists</label><label><input id="roomDampersR6" type="checkbox" checked> Motorized duct damper</label><small>R7 · blue 21 °C → green 24 °C → red 29 °C<br>Select a floor for room figures · click a room colour for CFM / grilles<br>DEMO per room · LIVE from the station points (r6 adapter)</small><a href="ALT_V79_RentalFloor.html" target="_blank" style="display:block;margin-top:8px">2D plan / CFM / damper per room</a>');
var r6Labels=[],damperGroups={},damperMeshes=[],r6Bounds=[];
roomCells.forEach(function(c){if(!c.room.numericLabel)return;var canvas=document.createElement('canvas');canvas.width=384;canvas.height=150;var tex=new THREE.CanvasTexture(canvas);tex.colorSpace=THREE.SRGBColorSpace;var sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true,depthTest:false,toneMapped:false}));
 sp.position.set((c.rect[0]+c.rect[2])/2,base(c.room.floor)+2.0,-(c.rect[1]+c.rect[3])/2);sp.scale.set(3.3,1.29,1);sp.renderOrder=30;sp.userData.roomCell=c.id;roomGroups[c.room.floor].add(sp);r6Labels.push({cell:c,canvas:canvas,tex:tex,sp:sp,last:''});
});
(plan.motorizedDampers||[]).forEach(function(d){var parent=damperGroups[d.floor];if(!parent){parent=damperGroups[d.floor]=new THREE.Group;S.LAYER.ducts.add(parent);}var g=new THREE.Group;parent.add(g);g.position.set(d.position[0],d.position[2],-d.position[1]);g.rotation.y=d.direction[0]?0:Math.PI/2;g.userData.damper=d.id;
 var w=d.w,h=d.h;hwMesh(new THREE.BoxGeometry(.12,h+.035,w+.035),mat.frame,g,new THREE.Vector3());var blade=hwMesh(new THREE.BoxGeometry(.022,h*.88,w*.88),mat.metal,g,new THREE.Vector3());if(!d.integralVAV)hwMesh(new THREE.BoxGeometry(.12,.12,.10),finish.actuator,g,new THREE.Vector3(0,h/2+.10,0));
 // Sleeve is a frame; remove solid centre so the blade is visible through the duct body.
 g.children[0].material=new THREE.MeshStandardMaterial({color:'#4f6570',wireframe:true,roughness:.7});damperMeshes.push({d:d,g:g,blade:blade,phase:damperMeshes.length*.71});g.updateWorldMatrix(true,true);var b=new THREE.Box3().setFromObject(g);r6Bounds.push({id:d.id,kind:'MOTORIZED-DAMPER',floor:d.floor,box:[b.min.x,-b.max.z,b.min.y,b.max.x,-b.min.z,b.max.y]});
});
var r6prevPR=S.applyFloor;S.applyFloor=function(){r6prevPR();r6Labels.forEach(function(l){l.sp.visible=S.$('roomReadingsR6').checked&&visibleFloor(l.cell.room.floor)&&S.ISO&&S.LAYER.zones.visible;});Object.keys(damperGroups).forEach(function(f){damperGroups[f].visible=visibleFloor(+f)&&S.$('roomDampersR6').checked&&S.LAYER.ducts.visible;});for(var k in S.ZONE){S.ZONE[k].g.visible=false;if(S.ZONE[k].sp)S.ZONE[k].sp.visible=false;}};
['roomReadingsR6','roomDampersR6'].forEach(function(k){S.$(k).addEventListener('change',S.applyFloor);});
function updateR6(){if(!demoFreeze)plan.roomSensors.forEach(function(s){var h=0;for(var ch of s.cell)h=(h*31+ch.charCodeAt(0))>>>0;var v=roomValues[s.cell];v.t=isRentalDemo()?21.7+(h%70)/10+.2*Math.sin(Date.now()/45000+(h%1000)/83):null;});
 for(var k in S.ZONE){S.ZONE[k].g.visible=false;if(S.ZONE[k].sp)S.ZONE[k].sp.visible=false;}
 roomCells.forEach(function(c){c.value=roomValues[c.id][S.METRIC];c.material.color.copy(roomColor(c.value,!isRentalDemo(),S.METRIC));c.material.opacity=c.state==='dedicated-demo'?.97:.80;});
 damperMeshes.forEach(function(x){var demo=isRentalDemo();x.blade.rotation.z=demo?(.25+.6*(.5+.5*Math.sin(performance.now()/6000+x.phase)))*Math.PI/2:0;x.blade.material.color.set(demo?'#8da9ad':'#65717b');x.g.userData.quality=demo?'DEMO':'Unbound';});
}
var priorR6Bv=S.updateZones;S.updateZones=function(t){priorR6Bv(t);updateR6();};
var priorOpenRoomR6=openRoomCell;openRoomCell=function(id){priorOpenRoomR6(id);var c=roomCells.find(function(c){return c.id===id;});if(!c)return;var r=c.room;S.$('info').insertAdjacentHTML('beforeend','<table><tr><td>Tenant</td><td>'+ (r.tenant||'COMMON')+'</td></tr><tr><td>Area</td><td>'+r.area_m2+' m²</td></tr><tr><td>Supply design</td><td>'+(r.supply_CFM? r.supply_CFM.toFixed(0)+' CFM':'—')+'</td></tr><tr><td>Supply outlets</td><td>'+(r.diffuserCount||0)+'</td></tr><tr><td>OA concept</td><td>'+(r.OA_target_Ls||'—')+' L/s</td></tr></table><p>Airflow / size are concept values from the load allowance; confirm load, NC, throw, ESP and TAB</p>');};
window.__R6={inspect:function(){return {revision:plan.revision,rooms:rooms.length,sensors:plan.roomSensors.length,tenancies:plan.tenancies.length,diffusers:plan.diffusers.length,dampers:damperMeshes.length,labels:r6Labels.length,visibleLabels:r6Labels.filter(function(l){return l.sp.visible;}).length,oldLabels:Object.values(S.ZONE).filter(function(o){return o.sp&&o.sp.visible;}).length,opacity:roomCells.map(function(c){return c.material.opacity;}),ordinaryStairs:plan.verticalTransport.ordinaryStairs};},labels:r6Labels,damperMeshes:damperMeshes,bounds:r6Bounds,openRoom:openRoomCell,refresh:function(){updateRental();updateR6();S.applyFloor();}};
updateR6();S.applyFloor();

// R7 airflow is driven by proven damper position AND measured airflow, never command alone.
controls.querySelector('h2').textContent='Equal companies / AHU all-air · R7';
document.querySelector('header h1').textContent='ALT Rental Office · Equal companies / AHU VAV · R7';
document.querySelector('header .sub').textContent='F02–F08 · A / B 888.69 m² each · identical room functions · no FCU';
S.$('roomReadingsR6').parentElement.lastChild.textContent=' Room labels · °C / RH / CO₂';
controls.insertAdjacentHTML('beforeend','<label><input id="airflowR7" type="checkbox" checked> Show airflow by damper feedback</label><label>DEMO room <select id="r7Room"></select></label><div style="display:flex;gap:6px"><button id="r7Open">Open room</button><button id="r7Close">Close room</button></div><small id="r7AirState"></small><a href="ALT_V79_AHU_AllAir.html" target="_blank">AHU / OA–RA–SA–EA / VSD / PICV</a>');
controls.querySelectorAll('label').forEach(function(l){l.style.display='block';});
var r7DeviceGroups={};/* r6: AHU air devices are drawn by devices79.js (Blender) */([]).forEach(function(d){var g=r7DeviceGroups[d.floor];if(!g){g=r7DeviceGroups[d.floor]=new THREE.Group;S.LAYER.air.add(g);}var pos=new THREE.Vector3(d.position[0],d.position[2],-d.position[1]);if(d.kind==='VSD'){hwMesh(new THREE.BoxGeometry(.42,.70,.24),mat.wall,g,pos);hwMesh(new THREE.PlaneGeometry(.20,.10),finish.screen,g,pos.clone().add(new THREE.Vector3(0,.14,.121)));for(var dy of [-.16,-.24])hwMesh(new THREE.BoxGeometry(.24,.02,.015),mat.frame,g,pos.clone().add(new THREE.Vector3(0,dy,.13)));}else if(d.kind==='AirMD'){hwMesh(new THREE.BoxGeometry(.28,.22,.26),finish.flange,g,pos);hwMesh(new THREE.BoxGeometry(.16,.12,.12),new THREE.MeshBasicMaterial({color:'#ca8c44',roughness:.55}),g,pos.clone().add(new THREE.Vector3(.20,.05,0)));hwMesh(new THREE.BoxGeometry(.025,.16,.20),finish.body,g,pos);}else{hwMesh(new THREE.BoxGeometry(.075,.065,.07),finish.body,g,pos.clone().add(new THREE.Vector3(0,.10,0)));hwMesh(S.cyl(.009,.16,8),finish.flange,g,pos.clone());}});
var r7Feedback={},r7DemoClosed={},r7Paths=[],r7AirGroups={};
plan.rooms.filter(r=>r.supply_CFM).forEach(r=>{S.$('r7Room').add(new Option(r.id+' · '+r.name,r.id));});
function r7State(id){if(isRentalDemo()){var r=plan.rooms.find(r=>r.id===id),closed=!!r7DemoClosed[id],design=r?(r.supply_CFM||(r.exhaust_Ls_concept||0)*2.11888):0,min=r?(r.minimumSA_CFM_concept||0):0,pct=r&&r.supply_CFM?Math.round(100*Math.min(1,Math.max(.65,design?min/design:0))):100;return {quality:'demo',position_pct:closed?0:pct,airflow_cfm:closed?0:Math.min(design,Math.max(design*pct/100,min))};}return r7Feedback[id]||{quality:'unbound',position_pct:null,airflow_cfm:null};}
function r7Flow(id){var v=r7State(id);return (v.quality==='good'||v.quality==='demo')&&Number.isFinite(v.position_pct)&&Number.isFinite(v.airflow_cfm)&&v.position_pct>5&&v.position_pct<=100&&v.airflow_cfm>1;}
plan.ducts.filter(d=>d.floor<9&&d.service==='SA'&&!d.id.startsWith('BR-')).forEach(function(d){
 var group=r7AirGroups[d.floor];if(!group){group=r7AirGroups[d.floor]=new THREE.Group;S.LAYER.ducts.add(group);}var lengths=[],total=0;for(var i=1;i<d.points.length;i++){var len=Math.hypot(...d.points[i].map((v,k)=>v-d.points[i-1][k]));lengths.push(len);total+=len;}
 if(!total)return;var glyphs=[];for(var i=0;i<2;i++){var o=S.mesh(new THREE.BoxGeometry(.18,.065,.065),new THREE.MeshBasicMaterial({color:'#59d6ff',transparent:true,opacity:.94,depthTest:false,toneMapped:false}),group);o.renderOrder=24;glyphs.push(o);}r7Paths.push({d:d,lengths:lengths,total:total,glyphs:glyphs});
});
function updateR7(){
 if(!demoFreeze)plan.roomSensors.forEach(function(s){var h=0;for(var ch of s.cell)h=(h*31+ch.charCodeAt(0))>>>0;var v=roomValues[s.cell];v.h=isRentalDemo()?47+(h%180)/10+2*Math.sin(Date.now()/55000+(h%1000)/83):null;v.c=isRentalDemo()?450+(h%530)+20*Math.sin(Date.now()/60000+(h%1000)/83):null;});
 var active=0,unknown=0;plan.rooms.filter(r=>r.supply_CFM).forEach(r=>{if(r7Flow(r.id))active++;if(r7State(r.id).quality==='unbound')unknown++;});
 damperMeshes.forEach(function(x){var s=r7State(x.d.room),good=s.quality==='demo'||s.quality==='good';var pos=good?s.position_pct:0;x.blade.rotation.z=pos/100*Math.PI/2;x.g.userData.quality=good?s.quality.toUpperCase():'Unbound';x.g.userData.feedback_pct=good?pos:null;x.blade.material.color.set(good?(pos>5?'#32b58c':'#c5734c'):'#65717b');});
 var now=performance.now()/1000;
 r7Paths.forEach(function(p){var ids=p.d.servedRooms||(p.d.room?[p.d.room]:plan.rooms.filter(r=>r.floor===p.d.floor&&r.supply_CFM).map(r=>r.id));var moving=ids.some(r7Flow)&&S.$('airflowR7').checked&&S.LAYER.ducts.visible&&visibleFloor(p.d.floor);
  p.glyphs.forEach(function(o,j){o.visible=moving;if(!moving)return;var dist=(now*1.2+j*p.total/2)%p.total,seg=0;while(seg<p.lengths.length-1&&dist>p.lengths[seg]){dist-=p.lengths[seg];seg++;}var a=p.d.points[seg],b=p.d.points[seg+1],t=dist/p.lengths[seg];o.position.set(a[0]+(b[0]-a[0])*t,a[2]+(b[2]-a[2])*t,-a[1]-(b[1]-a[1])*t);o.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0),new THREE.Vector3(b[0]-a[0],b[2]-a[2],a[1]-b[1]).normalize());});
 });
 // Translucent service casing keeps the internal airflow visible without recoloring galvanized ductwork.
 for(var f in storeys)storeys[f].ducts.traverse(function(o){if(o.isMesh&&o.userData.designKind==='duct'){o.material.transparent=S.$('airflowR7').checked;o.material.opacity=S.$('airflowR7').checked?.58:1;o.material.depthWrite=!S.$('airflowR7').checked;}});
 if(window.__R9)r9PaintLabels();
 S.$('r7AirState').textContent=(isRentalDemo()?'DEMO feedback':'LIVE / proposed points')+' · active '+active+' · unbound '+unknown+' · position + airflow proof';
}
var prevR7Bv=S.updateZones;S.updateZones=function(t){prevR7Bv(t);updateR7();};
var prevR7pr=S.applyFloor;S.applyFloor=function(){prevR7pr();Object.keys(r7DeviceGroups).forEach(f=>r7DeviceGroups[f].visible=visibleFloor(+f)&&S.LAYER.air.visible);Object.keys(r7AirGroups).forEach(f=>r7AirGroups[f].visible=visibleFloor(+f)&&S.$('airflowR7').checked&&S.LAYER.ducts.visible);};
S.$('airflowR7').onchange=()=>{S.applyFloor();updateR7();};
function toggleRoomR7(open){if(!isRentalDemo()){S.$('r7AirState').textContent='Turn on DEMO to try; this button never writes station commands';return;}r7DemoClosed[S.$('r7Room').value]=!open;updateR7();}
S.$('r7Open').onclick=()=>toggleRoomR7(true);S.$('r7Close').onclick=()=>toggleRoomR7(false);
window.__R7={feedback:r7Feedback,demoClosed:r7DemoClosed,paths:r7Paths,state:r7State,flow:r7Flow,setRoomDemo:function(id,open){r7DemoClosed[id]=!open;updateR7();},applyFeedback:function(id,v){if(!plan.rooms.some(r=>r.id===id))throw Error('Unknown room');r7Feedback[id]=v;updateR7();},refresh:function(){updateRental();updateR6();updateR7();S.applyFloor();},inspect:function(){return {revision:plan.revision,FCUs:plan.equipment.filter(e=>e.type==='fcu').length+window.MODEL.air_equipment.filter(e=>e.type==='fcu').length,companies:plan.tenancies.map(t=>({id:t.id,gross:t.grossExclusiveArea_m2,net:t.netRoomArea_m2,functions:t.functions})),movingPaths:r7Paths.filter(p=>p.glyphs.some(o=>o.visible)).length,labels:r6Labels.length,visibleLabels:r6Labels.filter(l=>l.sp.visible).length};}};
document.querySelector('[data-layer="air"]').parentElement.lastChild.textContent=' Air side / AHU / VSD / ventilation';S.$('officeTheme').value='day';applyTheme();window.__DESIGN.version=plan.revision;updateR7();S.applyFloor();

// Air is invisible: soft tinted tracer ribbons communicate measured direction, not CFD smoke.
r7Paths.forEach(function(p){p.glyphs.forEach(function(o){o.visible=false;o.parent.remove(o);});});r7Paths.length=0;
controls.querySelector('h2').textContent='Rental office / coordinated ceilings · R8';
document.querySelector('header h1').textContent='ALT Rental Office · Air distribution / EPMS ready · R8';
controls.insertAdjacentHTML('beforeend','<div style="display:flex;flex-wrap:wrap;gap:8px;font-size:11px;margin:10px 0"><span style="color:#238565">● OA / FA</span><span style="color:#168cb5">● SA</span><span style="color:#8865b8">● RA</span><span style="color:#c76b47">● EA / Toilet</span></div><label><input id="ceilingR8" type="checkbox"> Show ceilings / hide to see the plenum</label><a href="ALT_V79_Tenant_Metering.html" target="_blank">Tenant PM / BTU / EPMS interface</a>');
var r8Paths=[],r8Jets=[],r8AHUFeedback={},r8SensorValues={},r8SensorGroups={},r8Ceilings={},r8SeatAudit=window.__SEAT_AUDIT||[];
var r8TextureCanvas=document.createElement('canvas');r8TextureCanvas.width=128;r8TextureCanvas.height=32;
var r8ctx=r8TextureCanvas.getContext('2d'),r8grad=r8ctx.createRadialGradient(80,16,1,64,16,64);r8grad.addColorStop(0,'rgba(255,255,255,1)');r8grad.addColorStop(.3,'rgba(255,255,255,.85)');r8grad.addColorStop(.65,'rgba(255,255,255,.35)');r8grad.addColorStop(1,'rgba(255,255,255,0)');r8ctx.fillStyle=r8grad;r8ctx.fillRect(0,0,128,32);var softPixels=r8ctx.createImageData(128,32);for(var sy=0;sy<32;sy++)for(var sx=0;sx<128;sx++){var si=(sy*128+sx)*4,tail=Math.pow(Math.sin(Math.PI*sx/127),1.4),edge=Math.pow(Math.sin(Math.PI*sy/31),4),wisps=.72+.28*Math.sin(sx*.11+sy*.25);softPixels.data[si]=softPixels.data[si+1]=softPixels.data[si+2]=255;softPixels.data[si+3]=Math.round(255*tail*edge*wisps);}r8ctx.putImageData(softPixels,0,0);var r8Tex=new THREE.CanvasTexture(r8TextureCanvas);r8Tex.needsUpdate=true;
var r8Bundles=[];
function r8Ribbon(color,group){var g=new THREE.Group;group.userData.r8Bundles=group.userData.r8Bundles||{};var b=group.userData.r8Bundles[color];if(!b){b=group.userData.r8Bundles[color]={color:color,group:group,objects:[]};r8Bundles.push(b);}b.objects.push(g);return g;}
function r8Path(d,points,group){var lengths=[],total=0;for(var i=1;i<points.length;i++){var l=Math.hypot(...points[i].map((v,k)=>v-points[i-1][k]));lengths.push(l);total+=l;}if(total<.04)return;var count=Math.min(5,Math.max(1,Math.round(total/4))),glyphs=[];for(var j=0;j<count;j++)glyphs.push(r8Ribbon(plan.airColors[d.service]||'#cccccc',group));r8Paths.push({d:d,points:points,lengths:lengths,total:total,glyphs:glyphs});}
(plan.ductBodies||plan.ducts).forEach(function(d){var g=r7AirGroups[d.floor];if(!g){g=r7AirGroups[d.floor]=new THREE.Group;S.LAYER.ducts.add(g);}r8Path(d,d.flowDirection==='reverse'?d.points.slice().reverse():d.points,g);});
plan.diffusers.filter(t=>t.service==='SA').forEach(function(t){var g=r7AirGroups[t.floor];for(var k=0;k<1;k++)r8Jets.push({t:t,index:k,o:r8Ribbon(plan.airColors[t.service],g)});});
// One dynamic mesh per floor/service instead of thousands of individual particle draw calls.
r8Bundles.forEach(function(b){var cube=new THREE.BoxGeometry(1,1,1),pc=cube.attributes.position.constructor,uc=cube.attributes.uv.constructor,geo=new THREE.BoxGeometry(1,1,1),n=b.objects.length,uv=[],idx=[];b.positions=new Float32Array(n*24);var normals=new Float32Array(n*24);for(var i=0;i<n;i++){for(var k=0;k<2;k++){uv.push(0,0,1,0,1,1,0,1);var j=i*8+k*4;idx.push(j,j+1,j+2,j,j+2,j+3);for(var q=0;q<4;q++)normals[(j+q)*3+2]=1;}}geo.setAttribute('position',new pc(b.positions,3));b.positions=geo.attributes.position.array;geo.setAttribute('normal',new pc(normals,3));geo.setAttribute('uv',new uc(new Float32Array(uv),2));geo.setIndex(idx);geo.clearGroups();b.geometry=geo;b.mesh=S.mesh(geo,new THREE.MeshBasicMaterial({color:b.color,map:r8Tex,transparent:true,opacity:.83,depthWrite:false,side:THREE.DoubleSide,toneMapped:false}),b.group);b.mesh.frustumCulled=false;b.mesh.userData.r8Tracer=true;cube.dispose();});
function r8Batch(){var v=new THREE.Vector3(),corners=[[-.55,-.09,0],[.55,-.09,0],[.55,.09,0],[-.55,.09,0],[-.55,0,-.09],[.55,0,-.09],[.55,0,.09],[-.55,0,.09]];r8Bundles.forEach(function(b){var any=false;b.objects.forEach(function(o,i){var offset=i*24;if(!o.visible){b.positions.fill(0,offset,offset+24);return;}any=true;for(var j=0;j<8;j++){v.set(corners[j][0]*o.scale.x,corners[j][1]*o.scale.y,corners[j][2]*o.scale.z).applyQuaternion(o.quaternion).add(o.position);b.positions[offset+j*3]=v.x;b.positions[offset+j*3+1]=v.y;b.positions[offset+j*3+2]=v.z;}});b.mesh.visible=any;b.geometry.attributes.position.needsUpdate=true;});}
function r8Valid(v){return v&&['good','demo'].includes(v.quality)&&Number.isFinite(v.position_pct)&&v.position_pct>5&&v.position_pct<=100&&Number.isFinite(v.airflow_cfm)&&v.airflow_cfm>1&&(v.quality==='demo'||(Number.isFinite(v.timestamp)&&Date.now()-v.timestamp>=0&&Date.now()-v.timestamp<=30000));}
function r8Moving(d){if(d.room)return r8Valid(r7State(d.room));var ids=d.servedRooms||plan.rooms.filter(r=>r.supply_CFM&&(d.floor===9||r.floor===d.floor)).map(r=>r.id);if(['SA','RA'].includes(d.service))return ids.some(id=>r8Valid(r7State(id)));if(isRentalDemo())return d.service==='TE'||d.service==='KE'||d.service==='MA'||d.service==='PA'||d.service==='PE'||ids.some(id=>r8Valid(r7State(id)));return r8Valid(r8AHUFeedback[d.id]);}
function r8At(p,dist){var s=0;while(s<p.lengths.length-1&&dist>p.lengths[s]){dist-=p.lengths[s];s++;}var a=p.points[s],b=p.points[s+1],t=dist/p.lengths[s],rad=Math.min(.12,p.d.h/3,p.d.w/5),corner=null,u=null,v=null;
 if(s>0&&dist<rad){corner=a;u=p.points[s-1];v=b;t=(dist+rad)/(2*rad);}else if(s<p.lengths.length-1&&dist>p.lengths[s]-rad){corner=b;u=a;v=p.points[s+2];t=(dist-p.lengths[s]+rad)/(2*rad);}
 if(corner){var c=new THREE.Vector3(corner[0],corner[2],-corner[1]),first=new THREE.Vector3(corner[0]-u[0],corner[2]-u[2],u[1]-corner[1]).normalize(),last=new THREE.Vector3(v[0]-corner[0],v[2]-corner[2],corner[1]-v[1]).normalize(),start=c.clone().addScaledVector(first,-rad),end=c.clone().addScaledVector(last,rad),pos=start.clone().multiplyScalar((1-t)*(1-t)).addScaledVector(c,2*(1-t)*t).addScaledVector(end,t*t),dir=c.clone().sub(start).multiplyScalar(1-t).addScaledVector(end.clone().sub(c),t).normalize();return {position:pos,direction:dir};}
 return {position:new THREE.Vector3(a[0]+(b[0]-a[0])*t,a[2]+(b[2]-a[2])*t,-a[1]-(b[1]-a[1])*t),direction:new THREE.Vector3(b[0]-a[0],b[2]-a[2],a[1]-b[1]).normalize()};}
function r8Animate(){var enabled=S.$('airflowR7').checked&&S.LAYER.ducts.visible,now=performance.now()/1000;
 r8Paths.forEach(function(p){var show=enabled&&visibleFloor(p.d.floor)&&r8Moving(p.d);p.glyphs.forEach(function(o,j){o.visible=show;if(!show)return;var speed=Math.max(.7,Math.min(2.5,(p.d.velocity_ms||2)*.45)),dist=(now*speed+j*p.total/p.glyphs.length)%p.total,q=r8At(p,dist);var side=new THREE.Vector3().crossVectors(q.direction,new THREE.Vector3(0,1,0));if(side.length()<.1)side.set(1,0,0);side.normalize();var up=new THREE.Vector3().crossVectors(side,q.direction).normalize(),phase=j*2.399+now*.8;var al=Math.max(.2,Math.min(.42,Math.min(p.d.w,p.d.h)*1.1));o.position.copy(q.position);o.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0),q.direction);o.scale.set(al/1.1,al*.8/.18,al*.8/.18);});});
 r8Jets.forEach(function(j){var t=j.t,show=enabled&&visibleFloor(t.floor)&&S.FSEL!=='all'&&S.FSEL!=='roof'&&r8Valid(r7State(t.room));j.o.visible=show;if(!show)return;var u=(now*.43+j.index/3)%1,ang=j.index*Math.PI*2/3,reach=t.service==='SA'?u:1-u,spread=.06+reach*.34,drop=.06+reach*.8,p=t.position;j.o.position.set(p[0],p[2]-.1-u*.5,-p[1]);j.o.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0),new THREE.Vector3(0,-1,0));var js=.24*(1-u*.45);j.o.scale.set(js/1.1,js*.8/.18,js*.8/.18);});r8Batch();
}
// Distinct corridor sensors: represented on the wall with a clickable T/RH/CO2 card.
plan.corridorSensors.forEach(function(s){var g=r8SensorGroups[s.floor];if(!g){g=r8SensorGroups[s.floor]=new THREE.Group;S.LAYER.air.add(g);}var p=new THREE.Vector3(s.position[0],s.position[2],-s.position[1]);var unit=new THREE.Group;g.add(unit);unit.position.copy(p);unit.userData.corridorSensor=s.id;hwMesh(new THREE.BoxGeometry(.12,.12,.035),mat.wall,unit,new THREE.Vector3(0,0,0));hwMesh(new THREE.PlaneGeometry(.075,.035),mat.screen,unit,new THREE.Vector3(0,.016,.018));var c=document.createElement('canvas');c.width=320;c.height=130;var tex=new THREE.CanvasTexture(c),sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,depthTest:false,transparent:true}));sp.position.set(0,.55,0);sp.scale.set(2.8,1.14,1);unit.add(sp);r8SensorValues[s.id]={s:s,canvas:c,tex:tex,unit:unit,temperature_C:null,RH_pct:null,CO2_ppm:null,quality:'unbound'};});
function r8UpdateSensors(){Object.values(r8SensorValues).forEach(function(v){var s=v.s,h=0;for(var ch of s.id)h=(h*31+ch.charCodeAt(0))>>>0;var demo=isRentalDemo();v.temperature_C=demo?23+h%30/10:null;v.RH_pct=demo?48+h%100/10:null;v.CO2_ppm=demo?480+h%300:null;v.quality=demo?'demo':'unbound';var key=[v.quality,v.temperature_C,v.RH_pct,v.CO2_ppm].join('|');if(v.last===key)return;v.last=key;var c=v.canvas.getContext('2d');c.fillStyle='rgba(25,41,48,.94)';c.fillRect(0,0,320,130);c.fillStyle='#d8e4e4';c.font='17px Segoe UI';c.fillText(s.id,10,26);c.fillStyle='#fff';c.font='bold 29px Segoe UI';c.fillText(demo?v.temperature_C.toFixed(1)+' °C':'— / unbound',10,65);c.font='18px Segoe UI';c.fillText(demo?'RH '+v.RH_pct.toFixed(0)+'% · CO₂ '+v.CO2_ppm+' ppm':'RH — · CO₂ —',10,98);c.font='12px Segoe UI';c.fillText(demo?'DEMO / corridor sensor':'Proposed / no station ORD',10,119);v.tex.needsUpdate=true;});}
// Separate ceiling layer. Opening strips preserve the ceiling terminal faces and maintenance view.
plan.rooms.filter(r=>r.floor>=1&&r.floor<=8&&r.kind!=='mechanical').forEach(function(r){var f=r.floor,g=r8Ceilings[f];if(!g){g=r8Ceilings[f]=new THREE.Group;S.LAYER.shell.add(g);}var a=r.rect,z=base(f)+(f===1?3.2:2.7)+.025;var b=batch(g,f,'ceiling',true);var holes=plan.diffusers.filter(t=>t.room===r.id&&t.service!=='TA').map(t=>[t.position[0]-t.face_m[0]/2-.025,t.position[1]-t.face_m[1]/2-.025,t.position[0]+t.face_m[0]/2+.025,t.position[1]+t.face_m[1]/2+.025]);var xx=[a[0],a[2],...holes.flatMap(h=>[Math.max(a[0],h[0]),Math.min(a[2],h[2])])].sort((x,y)=>x-y),yy=[a[1],a[3],...holes.flatMap(h=>[Math.max(a[1],h[1]),Math.min(a[3],h[3])])].sort((x,y)=>x-y);for(var i=1;i<xx.length;i++)for(var j=1;j<yy.length;j++){var x=(xx[i]+xx[i-1])/2,y=(yy[j]+yy[j-1])/2;if(holes.some(h=>x>h[0]&&x<h[2]&&y>h[1]&&y<h[3]))continue;b.box('wall',x,z,y,xx[i]-xx[i-1],.045,yy[j]-yy[j-1],0,true);}b.flush();});
// Reserved physical electricity meter at each tenant feeder; thermal boundary stays explicitly unresolved.
plan.tenantMetering.forEach(function(t){var g=r8SensorGroups[t.floor],p=t.powerPosition;hwMesh(new THREE.BoxGeometry(.24,.34,.14),finish.body,g,new THREE.Vector3(p[0],p[2],-p[1]));hwMesh(new THREE.PlaneGeometry(.16,.08),mat.screen,g,new THREE.Vector3(p[0],p[2]+.04,-p[1]+.071));});
var prevR8Bv=S.updateZones;S.updateZones=function(t){prevR8Bv(t);r8Animate();r8UpdateSensors();};var prevR8pr=S.applyFloor;S.applyFloor=function(){prevR8pr();Object.keys(r8SensorGroups).forEach(f=>r8SensorGroups[f].visible=visibleFloor(+f)&&S.LAYER.air.visible);Object.keys(r8Ceilings).forEach(f=>r8Ceilings[f].visible=visibleFloor(+f)&&S.LAYER.shell.visible&&S.$('ceilingR8').checked);};S.$('ceilingR8').onchange=S.applyFloor;
var oldFeedback=window.__R7.applyFeedback;window.__R7.applyFeedback=function(id,v){oldFeedback(id,Object.assign({timestamp:Date.now()},v));};r7Flow=function(id){return r8Valid(r7State(id));};
window.__R7.flow=r7Flow;
window.__R8={paths:r8Paths,jets:r8Jets,sensors:r8SensorValues,ceilings:r8Ceilings,moving:r8Moving,valid:r8Valid,seatAudit:r8SeatAudit,applyServiceFeedback:function(id,v){if(!plan.ducts.some(d=>d.id===id))throw Error('Unknown duct');r8AHUFeedback[id]=Object.assign({timestamp:Date.now()},v);},refresh:function(){__R7.refresh();r8Animate();r8UpdateSensors();S.applyFloor();},inspect:function(){return {revision:plan.revision,airServices:[...new Set(r8Paths.map(p=>p.d.service))],moving:r8Paths.filter(p=>p.glyphs.some(o=>o.visible)).length,corridorSensors:plan.corridorSensors.length,ceilingVisible:S.$('ceilingR8').checked,tenantMeters:plan.tenantMetering.length};}};__R8.refresh();


// R9: visible airflow inspection and room-metric colors use the same values/palette.
controls.querySelector('h2').textContent='Room HVAC / airflow inspection · R9';
document.querySelector('header h1').textContent='ALT Rental Office · Coordinated ducts / room conditions · R9';
controls.insertAdjacentHTML('beforeend','<label><input id="airXrayR9" type="checkbox" checked> Transparent ducts / airflow inside</label><small>Air colours by service · labels use the room colour of the selected metric °C / RH / CO₂<br>Air tracers show direction and feedback; the speed is not a CFD result</small>');
function r9InspectMaterials(){var inspect=S.$('airXrayR9').checked&&S.$('airflowR7').checked;for(var f in storeys)storeys[f].ducts.traverse(function(o){if(o.isMesh&&o.userData.designKind==='duct'){o.material.transparent=inspect;o.material.opacity=inspect?.14:1;o.material.depthWrite=!inspect;o.renderOrder=inspect?8:0;}});r8Bundles.forEach(function(b){b.mesh.material.depthTest=!inspect;b.mesh.material.depthWrite=false;b.mesh.renderOrder=inspect?21:0;});}
function r9PaintLabels(){r6Labels.forEach(function(l){var v=roomValues[l.cell.id],s=r7State(l.cell.id),col=l.cell.material.color.getHexString(),metric=S.METRIC==='h'?'RH':S.METRIC==='c'?'CO₂':'TEMP',value=v[S.METRIC],unit=S.METRIC==='h'?' %RH':S.METRIC==='c'?' ppm':' °C',mode=isRentalDemo()?'DEMO':r8Valid(s)?'Feedback good':'LIVE unbound',key=[S.METRIC,col,v.t,v.h,v.c,mode,s.position_pct].join('|');if(l.r9key===key)return;l.r9key=key;var c=l.canvas;if(c.height!==180)c.height=180;var ctx=c.getContext('2d');ctx.fillStyle='#'+col;ctx.fillRect(0,0,384,180);ctx.fillStyle='#ffffff';ctx.font='600 19px Segoe UI';ctx.fillText(l.cell.room.name.slice(0,34),12,27);ctx.font='700 38px Segoe UI';ctx.fillText(value===null?'—':value.toFixed(S.METRIC==='t'?1:0)+unit,12,77);ctx.font='20px Segoe UI';ctx.fillText(S.METRIC==='t'?'RH '+(v.h===null?'—':v.h.toFixed(0))+'% · CO₂ '+(v.c===null?'—':v.c.toFixed(0))+' ppm':S.METRIC==='h'?(v.t===null?'—':v.t.toFixed(1))+' °C · CO₂ '+(v.c===null?'—':v.c.toFixed(0))+' ppm':(v.t===null?'—':v.t.toFixed(1))+' °C · RH '+(v.h===null?'—':v.h.toFixed(0))+'%',12,113);ctx.font='16px Segoe UI';ctx.fillText(metric+' · '+mode+' · MD '+(r8Valid(s)?s.position_pct+'%':'—'),12,155);l.tex.needsUpdate=true;l.r9color='#'+col;l.r9metric=S.METRIC;});
 Object.values(r8SensorValues).forEach(function(v){var val=S.METRIC==='h'?v.RH_pct:S.METRIC==='c'?v.CO2_ppm:v.temperature_C,col=roomColor(val,v.quality!=='demo'&&v.quality!=='good',S.METRIC).getHexString(),key=[S.METRIC,col,v.last].join('|');if(v.r9key===key)return;v.r9key=key;var c=v.canvas.getContext('2d');c.fillStyle='#'+col;c.fillRect(0,0,320,130);c.fillStyle='#fff';c.font='16px Segoe UI';c.fillText(v.s.id,10,24);c.font='bold 28px Segoe UI';c.fillText(val===null?'— / unbound':val.toFixed(S.METRIC==='t'?1:0)+(S.METRIC==='h'?' %RH':S.METRIC==='c'?' ppm':' °C'),10,64);c.font='17px Segoe UI';c.fillText(S.METRIC==='t'?'RH '+(v.RH_pct??'—')+'% · CO₂ '+(v.CO2_ppm??'—')+' ppm':(v.temperature_C===null?'—':v.temperature_C.toFixed(1))+' °C · '+(S.METRIC==='h'?'CO₂ '+(v.CO2_ppm??'—')+' ppm':'RH '+(v.RH_pct??'—')+'%'),10,96);c.font='12px Segoe UI';c.fillText(v.quality==='demo'?'DEMO / corridor sensor':'Proposed / no station ORD',10,119);v.tex.needsUpdate=true;v.r9color='#'+col;});}
var prevR9Bv=S.updateZones;S.updateZones=function(t){prevR9Bv(t);r9InspectMaterials();r9PaintLabels();};
var prevR9Refresh=window.__R8.refresh;window.__R8.refresh=function(){prevR9Refresh();r9InspectMaterials();r9PaintLabels();};S.$('airXrayR9').onchange=window.__R8.refresh;
window.__R9={refresh:window.__R8.refresh,paths:r8Paths,jets:r8Jets,labels:r6Labels,plan:plan,setMetric:function(k){if(!['t','h','c'].includes(k))throw Error('Unknown metric');S.METRIC=k;S.$('zmetric').value=k;window.__R8.refresh();},inspect:function(){return {revision:plan.revision,physicalDuctBodies:plan.ductBodies.length,mergedShells:plan.ductShells.length,moving:r8Paths.filter(p=>p.glyphs.some(g=>g.visible)).length,metric:S.METRIC,inspection:S.$('airXrayR9').checked};}};window.__R8.refresh();
window.__R9.viewClose=function(f){focus(String(f));S.flyTo([31,base(f)+18,11],[17,base(f)+2.7,-12]);};

window.__R9.bundles=r8Bundles;window.__R9.renderNow=function(){S.renderer.render(S.scene,S.camera);};

// Runtime audit uses the same boxes rendered here, including walls and furniture.
window.__OFFICE={plan:plan,boxes:boxes,omitted:omitted,focus:focus,inspect:function(){return {revision:plan.revision,floor:S.FSEL,isolation:S.ISO,theme:S.$('officeTheme').value,visibleFloors:Object.keys(storeys).filter(function(f){return storeys[f].structural.visible;}),tenantSuites:rooms.filter(function(r){return r.kind==='office'&&r.floor>1;}).length,rooms:rooms.length,proposedEquipment:plan.equipment.length,render:S.renderer.info.render};}};
// ------------------------------------------------------------------ r7: calmer airflow, readable room cards, no overlapping labels
// Air tracers: one small chevron every ~4 m of duct (max 5 per run) moving with the air, coloured by service, hidden behind walls;
// supply diffusers show one short down-arrow, only when a single floor is selected.
(function(){var c=r8TextureCanvas.getContext('2d'),W=r8TextureCanvas.width,H=r8TextureCanvas.height;c.clearRect(0,0,W,H);
 var P=function(u,v){return [u*W,v*H];};c.shadowColor='rgba(255,255,255,.9)';c.shadowBlur=4;c.fillStyle='#ffffff';c.beginPath();
 [[.16,.1],[.44,.1],[.84,.5],[.44,.9],[.16,.9],[.56,.5]].forEach(function(q,i){var p=P(q[0],q[1]);if(i)c.lineTo(p[0],p[1]);else c.moveTo(p[0],p[1]);});c.closePath();c.fill();r8Tex.needsUpdate=true;
 r8Bundles.forEach(function(b){b.mesh.material.opacity=.92;b.mesh.material.depthTest=true;});})();
var x7R7InspectBefore=r9InspectMaterials;r9InspectMaterials=function(){x7R7InspectBefore();r8Bundles.forEach(function(b){b.mesh.material.depthTest=true;b.mesh.renderOrder=9;});};
// Room / corridor cards: white card, dark text, the value and the side bar in the zone condition colour (same scale as the room fill)
function x7R7TextColor(col){var hsl={};col.getHSL(hsl);return new THREE.Color().setHSL(hsl.h,Math.max(.55,hsl.s),Math.min(.40,hsl.l));}
function x7R7Card(ctx,w,h,col,lines,grey){ctx.clearRect(0,0,w,h);var r=14;ctx.fillStyle='rgba(255,255,255,.96)';ctx.beginPath();ctx.moveTo(r,0);ctx.arcTo(w,0,w,h,r);ctx.arcTo(w,h,0,h,r);ctx.arcTo(0,h,0,0,r);ctx.arcTo(0,0,w,0,r);ctx.closePath();ctx.fill();
 ctx.lineWidth=3;ctx.strokeStyle='rgba(15,23,42,.28)';ctx.stroke();ctx.save();ctx.clip();ctx.fillStyle=grey?'#94a3b8':'#'+col.getHexString();ctx.fillRect(0,0,12,h);ctx.restore();
 var tc=grey?'#64748b':'#'+x7R7TextColor(col).getHexString(),y=0;lines.forEach(function(l){y+=l[1];ctx.font=l[0];ctx.fillStyle=l[2]==='v'?tc:l[2];ctx.fillText(l[3],24,y);});}
var x7R7Fix=function(v,d){return v===null||v===undefined||!isFinite(v)?'—':(+v).toFixed(d);};
r9PaintLabels=function(){var U={t:' °C',h:' %RH',c:' ppm'},D={t:1,h:0,c:0};
 r6Labels.forEach(function(l){var v=roomValues[l.cell.id],s=r7State(l.cell.id),col=l.cell.material.color,value=v[S.METRIC],mode=isRentalDemo()?'DEMO':r8Valid(s)?'LIVE':'LIVE unbound',grey=value===null||value===undefined,
  key=[S.METRIC,col.getHexString(),v.t,v.h,v.c,mode,s.position_pct].join('|');if(l.r9key===key)return;l.r9key=key;var c=l.canvas;if(c.height!==160)c.height=160;
  if(!l.r7scaled){l.sp.scale.set(2.5,1.04,1);l.r7scaled=true;}
  var other=S.METRIC==='t'?'RH '+x7R7Fix(v.h,0)+' % · CO₂ '+x7R7Fix(v.c,0)+' ppm':S.METRIC==='h'?x7R7Fix(v.t,1)+' °C · CO₂ '+x7R7Fix(v.c,0)+' ppm':x7R7Fix(v.t,1)+' °C · RH '+x7R7Fix(v.h,0)+' %';
  x7R7Card(c.getContext('2d'),384,160,col,[['600 19px Segoe UI',30,'#334155',l.cell.room.name.slice(0,30)],['700 44px Segoe UI',50,'v',grey?'—':x7R7Fix(value,D[S.METRIC])+U[S.METRIC]],['18px Segoe UI',32,'#334155',other],['14px Segoe UI',26,'#64748b',mode+(r8Valid(s)?' · damper '+s.position_pct+' %':'')]],grey);
  l.tex.needsUpdate=true;l.r9color='#'+col.getHexString();l.r9metric=S.METRIC;});
 Object.values(r8SensorValues).forEach(function(v){var val=S.METRIC==='h'?v.RH_pct:S.METRIC==='c'?v.CO2_ppm:v.temperature_C,grey=val===null||val===undefined,col=roomColor(val,v.quality!=='demo'&&v.quality!=='good',S.METRIC),key=[S.METRIC,col.getHexString(),v.last].join('|');if(v.r9key===key)return;v.r9key=key;
  var sp=v.unit.children.find(function(o){return o.isSprite;});if(sp&&!v.r7scaled){sp.scale.set(2.2,.9,1);v.r7scaled=true;v.sp=sp;}
  var other=S.METRIC==='t'?'RH '+x7R7Fix(v.RH_pct,0)+' % · CO₂ '+x7R7Fix(v.CO2_ppm,0)+' ppm':x7R7Fix(v.temperature_C,1)+' °C · '+(S.METRIC==='h'?'CO₂ '+x7R7Fix(v.CO2_ppm,0)+' ppm':'RH '+x7R7Fix(v.RH_pct,0)+' %');
  x7R7Card(v.canvas.getContext('2d'),320,130,col,[['600 15px Segoe UI',24,'#334155',v.s.id],['700 32px Segoe UI',38,'v',grey?'—':x7R7Fix(val,S.METRIC==='t'?1:0)+U[S.METRIC]],['15px Segoe UI',27,'#334155',other],['12px Segoe UI',22,'#64748b',v.quality==='demo'?'DEMO · corridor sensor':v.quality==='good'?'LIVE · corridor sensor':'LIVE unbound · corridor sensor']],grey);
  v.tex.needsUpdate=true;v.r9color='#'+col.getHexString();});};
// Overlap culling: nearest card first, a card that would cover one already shown is hidden; cards beyond 45 m are hidden
var x7R7Cull=0,x7R7V=new THREE.Vector3();
function x7R7Declutter(){var now=performance.now();if(now-x7R7Cull<180)return;x7R7Cull=now;var cam=S.camera,el=S.renderer.domElement,Wd=el.clientWidth,Hd=el.clientHeight,k=Hd/(2*Math.tan(cam.fov*Math.PI/360));
 var shown=function(o){for(var p=o.parent;p;p=p.parent)if(!p.visible)return false;return true;};
 var roomOK=S.$('roomReadingsR6').checked&&S.ISO&&S.LAYER.zones.visible;   // same rule as the R6 floor filter
 var all=r6Labels.map(function(l){return {sp:l.sp,ok:roomOK&&visibleFloor(l.cell.room.floor)};}).concat(Object.values(r8SensorValues).map(function(v){var sp=v.sp||v.unit.children.find(function(o){return o.isSprite;});return sp?{sp:sp,ok:true}:null;}).filter(Boolean));
 var list=[];all.forEach(function(a){var sp=a.sp;if(!a.ok||!shown(sp)){sp.visible=false;return;}sp.getWorldPosition(x7R7V);var d=x7R7V.distanceTo(cam.position);x7R7V.project(cam);
  if(x7R7V.z>1||d>45||Math.abs(x7R7V.x)>1.2||Math.abs(x7R7V.y)>1.2){sp.visible=false;return;}var w=sp.scale.x*k/d,h=sp.scale.y*k/d;list.push({sp:sp,d:d,x:(x7R7V.x+1)/2*Wd,y:(1-x7R7V.y)/2*Hd,w:w,h:h});});
 list.sort(function(a,b){return a.d-b.d;});var placed=[];list.forEach(function(r){var hit=placed.some(function(q){return Math.abs(r.x-q.x)*2<r.w+q.w+6&&Math.abs(r.y-q.y)*2<r.h+q.h+4;});r.sp.visible=!hit&&r.h>9;if(r.sp.visible)placed.push(r);});}
var x7PrevR7Bv=S.updateZones;S.updateZones=function(t){x7PrevR7Bv(t);x7R7Declutter();};
window.__R9.declutter=function(){x7R7Cull=0;x7R7Declutter();return {cards:r6Labels.length,shown:r6Labels.filter(function(l){return l.sp.visible;}).length};};
// ------------------------------------------------------------------ r6: LIVE adapter (station points -> R9 rooms / dampers / meters / services)
// The R9 layer shows nothing as LIVE unless it is measured: room T / RH / CO2 / occupancy from the room sensor points, VAV damper position
// AND measured airflow (R9 motion proof), floor power / BTU meters, OA ducts from the measured OA airflow + OA damper feedback.
// Values come from window.PTS (subscribed by scene79.js); unresolved points (S.FAIL) and points without a value stay 'unbound'.
// The timestamp is the time of this read while the station connection is up (the subscription keeps the values current).
(function(){
 var nm=function(x){return x.replace(/[^A-Za-z0-9]+/g,'_').replace(/^_|_$/g,'');},pad=function(n){return String(n).padStart(2,'0');};
 var num=function(k){var v=S.V[k];if(S.FAIL&&S.FAIL.has(k))return null;return typeof v==='number'&&isFinite(v)?v:typeof v==='boolean'?(v?100:0):null;};
 var CFM=2.11888;   // L/s -> CFM
 var serviceSrc={};  // duct body id -> function returning feedback or null
 (plan.ductBodies||[]).forEach(function(b){
  if(b.service!=='OA')return;
  if(b.floor>=2&&b.floor<=8){var u='AHU_F'+pad(b.floor);serviceSrc[b.id]=function(){var pos=num(u+'_OADmpFb'),fl=num(u+'_OAFlow');return pos===null||fl===null?null:{position_pct:pos,airflow_cfm:fl*CFM};};}
  else if(b.floor===9)serviceSrc[b.id]=function(){var hz=num('OAU01_SpeedFeedbackHz'),fl=num('OAU01_Airflow');return hz===null||fl===null?null:{position_pct:Math.min(100,hz/50*100),airflow_cfm:fl*CFM};};
 });
 S.r9Live=function(){
  if(isRentalDemo())return;var now=Date.now(),live=!S.DEMO&&/^LIVE/.test(S.$('mode').textContent);
  plan.roomSensors.forEach(function(s){var k='RM_'+nm(s.room),v=roomValues[s.cell];if(!v)return;
   v.t=live?num(k+'_T'):null;v.h=live?num(k+'_RH'):null;v.c=live?num(k+'_CO2'):null;var o=S.V[k+'_Occ'];v.o=live&&typeof o==='boolean'?o:null;
   v.quality=live&&(v.t!==null||v.h!==null||v.c!==null)?'good':'unbound';});
  roomCells.forEach(function(c){var v=roomValues[c.id];if(!v)return;var value=v[S.METRIC];c.value=typeof value==='number'&&isFinite(value)?value:null;
   c.state=v.quality==='good'?(c.value===null?'missing':'dedicated-live'):'unbound';c.material.color.copy(roomColor(c.value,v.quality!=='good',S.METRIC));c.material.opacity=c.state==='dedicated-live'?.97:.80;});
  plan.airTerminals.forEach(function(t){var p='VAV_'+nm(t.room),pos=num(p+'_DmpFb'),fl=num(p+'_Airflow');
   if(live&&pos!==null&&fl!==null)r7Feedback[t.room]={quality:'good',position_pct:pos,airflow_cfm:fl*CFM,timestamp:now};else delete r7Feedback[t.room];});
  for(var id in serviceSrc){var f=live?serviceSrc[id]():null;if(f)r8AHUFeedback[id]=Object.assign({quality:'good',timestamp:now},f);else delete r8AHUFeedback[id];}
  plan.floorMeters.forEach(function(m){var p='F'+pad(m.floor),v={quality:'unbound'};
   if(live){v={power_kW:num('PM_'+p+'_kW'),electric_kWh:num('PM_'+p+'_kWh'),thermal_kW:num('BTU_'+p+'_kW'),thermal_kWh:num('BTU_'+p+'_kWh'),supply_C:num('TT_S_'+p),return_C:num('TT_R_'+p),flow_m3h:num('FM_'+p+'_Flow')};
    v.quality=v.power_kW!==null||v.thermal_kW!==null?'good':'unbound';}
   floorMeterValues[m.floor]=Object.assign(floorMeterValues[m.floor]||{},v);});
  Object.values(r8SensorValues).forEach(function(v){var k='CS_'+nm(v.s.id.replace(/^CS-/,''));   // corridor sensors (v79_r6.corridor)
   v.temperature_C=live?num(k+'_T'):null;v.RH_pct=live?num(k+'_RH'):null;v.CO2_ppm=live?num(k+'_CO2'):null;
   v.quality=live&&v.temperature_C!==null?'good':'unbound';v.last=[v.quality,v.temperature_C,v.RH_pct,v.CO2_ppm].join('|');});
 };
 var prevLiveBv=S.updateZones;S.updateZones=function(t){prevLiveBv(t);if(!isRentalDemo()){S.r9Live();damperMeshes.forEach(function(x){var st=r7State(x.d.room),good=st.quality==='good';var pos=good?st.position_pct:0;x.blade.rotation.z=pos/100*Math.PI/2;x.blade.material.color.set(good?(pos>5?'#32b58c':'#c5734c'):'#65717b');});r9PaintLabels();}};
 window.__R9.live=function(){return {rooms:Object.values(roomValues).filter(function(v){return v.quality==='good';}).length,terminals:Object.keys(r7Feedback).length,services:Object.keys(r8AHUFeedback).length};};
})();
window.__DESIGN.version='OFFICE-B1-R5';focus('all');
})();



}
