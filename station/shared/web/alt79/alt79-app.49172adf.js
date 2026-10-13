(()=>{var Ni={LEFT:0,MIDDLE:1,RIGHT:2,ROTATE:0,DOLLY:1,PAN:2},ts={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},Em=0,Sd=1,bm=2;var yl=1,gh=2,ra=3,Es=0,Hn=1,mn=2,bs=0,Ui=1,oa=2,wd=3,Ad=4,Tm=5;var eo=100,Sm=101,wm=102,Am=103,Rm=104,Cm=200,Im=201,Pm=202,Lm=203,Rd=204,Cd=205,Dm=206,Nm=207,Um=208,Fm=209,Om=210,Bm=211,Hm=212,km=213,Vm=214,Bc=0,Hc=1,kc=2,Go=3,Vc=4,zc=5,Gc=6,Wc=7,Id=0,zm=1,Gm=2,ns=0,Pd=1,Ld=2,Dd=3,Ml=4,Nd=5,Ud=6,Fd=7,ud="attached",Wm="detached",Od=300,gr=301,to=302,_h=303,xh=304,El=306,oi=1e3,Ii=1001,Wo=1002,vn=1003,vh=1004;var no=1005;var yn=1006,aa=1007;var is=1008;var di=1009,Bd=1010,Hd=1011,la=1012,yh=1013,ss=1014,Ti=1015,rs=1016,Mh=1017,Eh=1018,ca=1020,kd=35902,Vd=35899,zd=1021,Gd=1022,Si=1023,xs=1026,_r=1027,bh=1028,Th=1029,xr=1030,Sh=1031;var wh=1033,bl=33776,Tl=33777,Sl=33778,wl=33779,Ah=35840,Rh=35841,Ch=35842,Ih=35843,Ph=36196,Lh=37492,Dh=37496,Nh=37488,Uh=37489,Al=37490,Fh=37491,Oh=37808,Bh=37809,Hh=37810,kh=37811,Vh=37812,zh=37813,Gh=37814,Wh=37815,Xh=37816,qh=37817,Yh=37818,$h=37819,Zh=37820,Kh=37821,jh=36492,Jh=36494,Qh=36495,eu=36283,tu=36284,Rl=36285,nu=36286;var Vr=2300,zr=2301,Uc=2302,dd=2303,fd=2400,pd=2401,md=2402,Xm=2500;var Wd=0,Cl=1,ha=2,qm=3200;var iu=0,Ym=1,$s="",sn="srgb",ti="srgb-linear",Ka="linear",Gt="srgb";var Fc=7680;var $m=519,Zm=512,Km=513,jm=514,su=515,Jm=516,Qm=517,ru=518,e0=519,Xd=35044;var qd="300 es",ji=2e3,Xo=2001;function jg(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Jg(n){return ArrayBuffer.isView(n)&&!(n instanceof DataView)}function qo(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function t0(){let n=qo("canvas");return n.style.display="block",n}var Lp={},Yo=null;function ja(...n){let e="THREE."+n.shift();Yo?Yo("log",e,...n):console.log(e,...n)}function n0(n){let e=n[0];if(typeof e=="string"&&e.startsWith("TSL:")){let t=n[1];t&&t.isStackTrace?n[0]+=" "+t.getLocation():n[1]='Stack trace not available. Enable "THREE.Node.captureStackTrace" to capture stack traces.'}return n}function nt(...n){n=n0(n);let e="THREE."+n.shift();if(Yo)Yo("warn",e,...n);else{let t=n[0];t&&t.isStackTrace?console.warn(t.getError(e)):console.warn(e,...n)}}function ht(...n){n=n0(n);let e="THREE."+n.shift();if(Yo)Yo("error",e,...n);else{let t=n[0];t&&t.isStackTrace?console.error(t.getError(e)):console.error(e,...n)}}function kr(...n){let e=n.join(" ");e in Lp||(Lp[e]=!0,nt(...n))}function i0(n,e,t){return new Promise(function(i,s){function r(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:s();break;case n.TIMEOUT_EXPIRED:setTimeout(r,t);break;default:i()}}setTimeout(r,t)})}var s0={[Bc]:Hc,[kc]:Gc,[Vc]:Wc,[Go]:zc,[Hc]:Bc,[Gc]:kc,[Wc]:Vc,[zc]:Go},Qi=class{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});let i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){let i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){let i=this._listeners;if(i===void 0)return;let s=i[e];if(s!==void 0){let r=s.indexOf(t);r!==-1&&s.splice(r,1)}}dispatchEvent(e){let t=this._listeners;if(t===void 0)return;let i=t[e.type];if(i!==void 0){e.target=this;let s=i.slice(0);for(let r=0,o=s.length;r<o;r++)s[r].call(this,e);e.target=null}}},qn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Dp=1234567,Vo=Math.PI/180,Gr=180/Math.PI;function Ji(){let n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(qn[n&255]+qn[n>>8&255]+qn[n>>16&255]+qn[n>>24&255]+"-"+qn[e&255]+qn[e>>8&255]+"-"+qn[e>>16&15|64]+qn[e>>24&255]+"-"+qn[t&63|128]+qn[t>>8&255]+"-"+qn[t>>16&255]+qn[t>>24&255]+qn[i&255]+qn[i>>8&255]+qn[i>>16&255]+qn[i>>24&255]).toLowerCase()}function St(n,e,t){return Math.max(e,Math.min(t,n))}function Yd(n,e){return(n%e+e)%e}function Qg(n,e,t,i,s){return i+(n-e)*(s-i)/(t-e)}function e_(n,e,t){return n!==e?(t-n)/(e-n):0}function Ya(n,e,t){return(1-t)*n+t*e}function t_(n,e,t,i){return Ya(n,e,1-Math.exp(-t*i))}function n_(n,e=1){return e-Math.abs(Yd(n,e*2)-e)}function i_(n,e,t){return n<=e?0:n>=t?1:(n=(n-e)/(t-e),n*n*(3-2*n))}function s_(n,e,t){return n<=e?0:n>=t?1:(n=(n-e)/(t-e),n*n*n*(n*(n*6-15)+10))}function r_(n,e){return n+Math.floor(Math.random()*(e-n+1))}function o_(n,e){return n+Math.random()*(e-n)}function a_(n){return n*(.5-Math.random())}function l_(n){n!==void 0&&(Dp=n);let e=Dp+=1831565813;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}function c_(n){return n*Vo}function h_(n){return n*Gr}function u_(n){return n>0&&Number.isInteger(n)&&2**Math.round(Math.log2(n))===n}function d_(n){return Math.pow(2,Math.ceil(Math.log(n)/Math.LN2))}function f_(n){return Math.pow(2,Math.floor(Math.log(n)/Math.LN2))}function p_(n,e,t,i,s){let r=Math.cos,o=Math.sin,a=r(t/2),c=o(t/2),l=r((e+i)/2),u=o((e+i)/2),d=r((e-i)/2),f=o((e-i)/2),p=r((i-e)/2),x=o((i-e)/2);switch(s){case"XYX":n.set(a*u,c*d,c*f,a*l);break;case"YZY":n.set(c*f,a*u,c*d,a*l);break;case"ZXZ":n.set(c*d,c*f,a*u,a*l);break;case"XZX":n.set(a*u,c*x,c*p,a*l);break;case"YXY":n.set(c*p,a*u,c*x,a*l);break;case"ZYZ":n.set(c*x,c*p,a*u,a*l);break;default:nt("MathUtils: .setQuaternionFromProperEuler() encountered an unknown order: "+s)}}function Ki(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:case Uint8ClampedArray:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("THREE.MathUtils: Invalid component type.")}}function Yt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:case Uint8ClampedArray:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("THREE.MathUtils: Invalid component type.")}}var Zs={DEG2RAD:Vo,RAD2DEG:Gr,generateUUID:Ji,clamp:St,euclideanModulo:Yd,mapLinear:Qg,inverseLerp:e_,lerp:Ya,damp:t_,pingpong:n_,smoothstep:i_,smootherstep:s_,randInt:r_,randFloat:o_,randFloatSpread:a_,seededRandom:l_,degToRad:c_,radToDeg:h_,isPowerOfTwo:u_,ceilPowerOfTwo:d_,floorPowerOfTwo:f_,setQuaternionFromProperEuler:p_,normalize:Yt,denormalize:Ki},Pe=class n{static{n.prototype.isVector2=!0}constructor(e=0,t=0){this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("THREE.Vector2: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("THREE.Vector2: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){let t=this.x,i=this.y,s=e.elements;return this.x=s[0]*t+s[3]*i+s[6],this.y=s[1]*t+s[4]*i+s[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=St(this.x,e.x,t.x),this.y=St(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=St(this.x,e,t),this.y=St(this.y,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(St(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let i=this.dot(e)/t;return Math.acos(St(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){let i=Math.cos(t),s=Math.sin(t),r=this.x-e.x,o=this.y-e.y;return this.x=r*i-o*s+e.x,this.y=r*s+o*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}},rn=class{constructor(e=0,t=0,i=0,s=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=s}static slerpFlat(e,t,i,s,r,o,a){let c=i[s+0],l=i[s+1],u=i[s+2],d=i[s+3],f=r[o+0],p=r[o+1],x=r[o+2],b=r[o+3];if(d!==b||c!==f||l!==p||u!==x){let g=c*f+l*p+u*x+d*b;g<0&&(f=-f,p=-p,x=-x,b=-b,g=-g);let m=1-a;if(g<.9995){let A=Math.acos(g),U=Math.sin(A);m=Math.sin(m*A)/U,a=Math.sin(a*A)/U,c=c*m+f*a,l=l*m+p*a,u=u*m+x*a,d=d*m+b*a}else{c=c*m+f*a,l=l*m+p*a,u=u*m+x*a,d=d*m+b*a;let A=1/Math.sqrt(c*c+l*l+u*u+d*d);c*=A,l*=A,u*=A,d*=A}}e[t]=c,e[t+1]=l,e[t+2]=u,e[t+3]=d}static multiplyQuaternionsFlat(e,t,i,s,r,o){let a=i[s],c=i[s+1],l=i[s+2],u=i[s+3],d=r[o],f=r[o+1],p=r[o+2],x=r[o+3];return e[t]=a*x+u*d+c*p-l*f,e[t+1]=c*x+u*f+l*d-a*p,e[t+2]=l*x+u*p+a*f-c*d,e[t+3]=u*x-a*d-c*f-l*p,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,s){return this._x=e,this._y=t,this._z=i,this._w=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){let i=e._x,s=e._y,r=e._z,o=e._order,a=Math.cos,c=Math.sin,l=a(i/2),u=a(s/2),d=a(r/2),f=c(i/2),p=c(s/2),x=c(r/2);switch(o){case"XYZ":this._x=f*u*d+l*p*x,this._y=l*p*d-f*u*x,this._z=l*u*x+f*p*d,this._w=l*u*d-f*p*x;break;case"YXZ":this._x=f*u*d+l*p*x,this._y=l*p*d-f*u*x,this._z=l*u*x-f*p*d,this._w=l*u*d+f*p*x;break;case"ZXY":this._x=f*u*d-l*p*x,this._y=l*p*d+f*u*x,this._z=l*u*x+f*p*d,this._w=l*u*d-f*p*x;break;case"ZYX":this._x=f*u*d-l*p*x,this._y=l*p*d+f*u*x,this._z=l*u*x-f*p*d,this._w=l*u*d+f*p*x;break;case"YZX":this._x=f*u*d+l*p*x,this._y=l*p*d+f*u*x,this._z=l*u*x-f*p*d,this._w=l*u*d-f*p*x;break;case"XZY":this._x=f*u*d-l*p*x,this._y=l*p*d-f*u*x,this._z=l*u*x+f*p*d,this._w=l*u*d+f*p*x;break;default:nt("Quaternion: .setFromEuler() encountered an unknown order: "+o)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){let i=t/2,s=Math.sin(i);return this._x=e.x*s,this._y=e.y*s,this._z=e.z*s,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){let t=e.elements,i=t[0],s=t[4],r=t[8],o=t[1],a=t[5],c=t[9],l=t[2],u=t[6],d=t[10],f=i+a+d;if(f>0){let p=.5/Math.sqrt(f+1);this._w=.25/p,this._x=(u-c)*p,this._y=(r-l)*p,this._z=(o-s)*p}else if(i>a&&i>d){let p=2*Math.sqrt(1+i-a-d);this._w=(u-c)/p,this._x=.25*p,this._y=(s+o)/p,this._z=(r+l)/p}else if(a>d){let p=2*Math.sqrt(1+a-i-d);this._w=(r-l)/p,this._x=(s+o)/p,this._y=.25*p,this._z=(c+u)/p}else{let p=2*Math.sqrt(1+d-i-a);this._w=(o-s)/p,this._x=(r+l)/p,this._y=(c+u)/p,this._z=.25*p}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<1e-8?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(St(this.dot(e),-1,1)))}rotateTowards(e,t){let i=this.angleTo(e);if(i===0)return this;let s=Math.min(1,t/i);return this.slerp(e,s),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){let i=e._x,s=e._y,r=e._z,o=e._w,a=t._x,c=t._y,l=t._z,u=t._w;return this._x=i*u+o*a+s*l-r*c,this._y=s*u+o*c+r*a-i*l,this._z=r*u+o*l+i*c-s*a,this._w=o*u-i*a-s*c-r*l,this._onChangeCallback(),this}slerp(e,t){let i=e._x,s=e._y,r=e._z,o=e._w,a=this.dot(e);a<0&&(i=-i,s=-s,r=-r,o=-o,a=-a);let c=1-t;if(a<.9995){let l=Math.acos(a),u=Math.sin(l);c=Math.sin(c*l)/u,t=Math.sin(t*l)/u,this._x=this._x*c+i*t,this._y=this._y*c+s*t,this._z=this._z*c+r*t,this._w=this._w*c+o*t,this._onChangeCallback()}else this._x=this._x*c+i*t,this._y=this._y*c+s*t,this._z=this._z*c+r*t,this._w=this._w*c+o*t,this.normalize();return this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){let e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),s=Math.sqrt(1-i),r=Math.sqrt(i);return this.set(s*Math.sin(e),s*Math.cos(e),r*Math.sin(t),r*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},y=class n{static{n.prototype.isVector3=!0}constructor(e=0,t=0,i=0){this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("THREE.Vector3: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("THREE.Vector3: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(Np.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(Np.setFromAxisAngle(e,t))}applyMatrix3(e){let t=this.x,i=this.y,s=this.z,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6]*s,this.y=r[1]*t+r[4]*i+r[7]*s,this.z=r[2]*t+r[5]*i+r[8]*s,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){let t=this.x,i=this.y,s=this.z,r=e.elements,o=1/(r[3]*t+r[7]*i+r[11]*s+r[15]);return this.x=(r[0]*t+r[4]*i+r[8]*s+r[12])*o,this.y=(r[1]*t+r[5]*i+r[9]*s+r[13])*o,this.z=(r[2]*t+r[6]*i+r[10]*s+r[14])*o,this}applyQuaternion(e){let t=this.x,i=this.y,s=this.z,r=e.x,o=e.y,a=e.z,c=e.w,l=2*(o*s-a*i),u=2*(a*t-r*s),d=2*(r*i-o*t);return this.x=t+c*l+o*d-a*u,this.y=i+c*u+a*l-r*d,this.z=s+c*d+r*u-o*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){let t=this.x,i=this.y,s=this.z,r=e.elements;return this.x=r[0]*t+r[4]*i+r[8]*s,this.y=r[1]*t+r[5]*i+r[9]*s,this.z=r[2]*t+r[6]*i+r[10]*s,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=St(this.x,e.x,t.x),this.y=St(this.y,e.y,t.y),this.z=St(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=St(this.x,e,t),this.y=St(this.y,e,t),this.z=St(this.z,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(St(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){let i=e.x,s=e.y,r=e.z,o=t.x,a=t.y,c=t.z;return this.x=s*c-r*a,this.y=r*o-i*c,this.z=i*a-s*o,this}projectOnVector(e){let t=e.lengthSq();if(t===0)return this.set(0,0,0);let i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return Fu.copy(this).projectOnVector(e),this.sub(Fu)}reflect(e){return this.sub(Fu.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let i=this.dot(e)/t;return Math.acos(St(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,i=this.y-e.y,s=this.z-e.z;return t*t+i*i+s*s}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){let s=Math.sin(t)*e;return this.x=s*Math.sin(i),this.y=Math.cos(t)*e,this.z=s*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){let t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),s=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=s,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}},Fu=new y,Np=new rn,gt=class n{static{n.prototype.isMatrix3=!0}constructor(e,t,i,s,r,o,a,c,l){this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,s,r,o,a,c,l)}set(e,t,i,s,r,o,a,c,l){let u=this.elements;return u[0]=e,u[1]=s,u[2]=a,u[3]=t,u[4]=r,u[5]=c,u[6]=i,u[7]=o,u[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){let t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){let t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let i=e.elements,s=t.elements,r=this.elements,o=i[0],a=i[3],c=i[6],l=i[1],u=i[4],d=i[7],f=i[2],p=i[5],x=i[8],b=s[0],g=s[3],m=s[6],A=s[1],U=s[4],T=s[7],I=s[2],L=s[5],P=s[8];return r[0]=o*b+a*A+c*I,r[3]=o*g+a*U+c*L,r[6]=o*m+a*T+c*P,r[1]=l*b+u*A+d*I,r[4]=l*g+u*U+d*L,r[7]=l*m+u*T+d*P,r[2]=f*b+p*A+x*I,r[5]=f*g+p*U+x*L,r[8]=f*m+p*T+x*P,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){let e=this.elements,t=e[0],i=e[1],s=e[2],r=e[3],o=e[4],a=e[5],c=e[6],l=e[7],u=e[8];return t*o*u-t*a*l-i*r*u+i*a*c+s*r*l-s*o*c}invert(){let e=this.elements,t=e[0],i=e[1],s=e[2],r=e[3],o=e[4],a=e[5],c=e[6],l=e[7],u=e[8],d=u*o-a*l,f=a*c-u*r,p=l*r-o*c,x=t*d+i*f+s*p;if(x===0)return this.set(0,0,0,0,0,0,0,0,0);let b=1/x;return e[0]=d*b,e[1]=(s*l-u*i)*b,e[2]=(a*i-s*o)*b,e[3]=f*b,e[4]=(u*t-s*c)*b,e[5]=(s*r-a*t)*b,e[6]=p*b,e[7]=(i*c-l*t)*b,e[8]=(o*t-i*r)*b,this}transpose(){let e,t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){let t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,s,r,o,a){let c=Math.cos(r),l=Math.sin(r);return this.set(i*c,i*l,-i*(c*o+l*a)+o+e,-s*l,s*c,-s*(-l*o+c*a)+a+t,0,0,1),this}scale(e,t){return kr("Matrix3: .scale() is deprecated. Use .makeScale() instead."),this.premultiply(Ou.makeScale(e,t)),this}rotate(e){return kr("Matrix3: .rotate() is deprecated. Use .makeRotation() instead."),this.premultiply(Ou.makeRotation(-e)),this}translate(e,t){return kr("Matrix3: .translate() is deprecated. Use .makeTranslation() instead."),this.premultiply(Ou.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){let t=this.elements,i=e.elements;for(let s=0;s<9;s++)if(t[s]!==i[s])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){let i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}},Ou=new gt,Up=new gt().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),Fp=new gt().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function m_(){let n={enabled:!0,workingColorSpace:ti,spaces:{},convert:function(s,r,o){return this.enabled===!1||r===o||!r||!o||(this.spaces[r].transfer===Gt&&(s.r=ks(s.r),s.g=ks(s.g),s.b=ks(s.b)),this.spaces[r].primaries!==this.spaces[o].primaries&&(s.applyMatrix3(this.spaces[r].toXYZ),s.applyMatrix3(this.spaces[o].fromXYZ)),this.spaces[o].transfer===Gt&&(s.r=zo(s.r),s.g=zo(s.g),s.b=zo(s.b))),s},workingToColorSpace:function(s,r){return this.convert(s,this.workingColorSpace,r)},colorSpaceToWorking:function(s,r){return this.convert(s,r,this.workingColorSpace)},getPrimaries:function(s){return this.spaces[s].primaries},getTransfer:function(s){return s===$s?Ka:this.spaces[s].transfer},getToneMappingMode:function(s){return this.spaces[s].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(s,r=this.workingColorSpace){return s.fromArray(this.spaces[r].luminanceCoefficients)},define:function(s){Object.assign(this.spaces,s)},_getMatrix:function(s,r,o){return s.copy(this.spaces[r].toXYZ).multiply(this.spaces[o].fromXYZ)},_getDrawingBufferColorSpace:function(s){return this.spaces[s].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(s=this.workingColorSpace){return this.spaces[s].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(s,r){return kr("ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),n.workingToColorSpace(s,r)},toWorkingColorSpace:function(s,r){return kr("ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),n.colorSpaceToWorking(s,r)}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[ti]:{primaries:e,whitePoint:i,transfer:Ka,toXYZ:Up,fromXYZ:Fp,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:sn},outputColorSpaceConfig:{drawingBufferColorSpace:sn}},[sn]:{primaries:e,whitePoint:i,transfer:Gt,toXYZ:Up,fromXYZ:Fp,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:sn}}}),n}var It=m_();function ks(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function zo(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}var bo,Xc=class{static getDataURL(e,t="image/png"){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let i;if(e instanceof HTMLCanvasElement)i=e;else{bo===void 0&&(bo=qo("canvas")),bo.width=e.width,bo.height=e.height;let s=bo.getContext("2d");e instanceof ImageData?s.putImageData(e,0,0):s.drawImage(e,0,0,e.width,e.height),i=bo}return i.toDataURL(t)}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){let t=qo("canvas");t.width=e.width,t.height=e.height;let i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);let s=i.getImageData(0,0,e.width,e.height),r=s.data;for(let o=0;o<r.length;o++)r[o]=ks(r[o]/255)*255;return i.putImageData(s,0,0),t}else if(e.data){let t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(ks(t[i]/255)*255):t[i]=ks(t[i]);return{data:t,width:e.width,height:e.height}}else return nt("ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}},g_=0,$o=class{constructor(e=null){this.isTextureSource=!0,Object.defineProperty(this,"id",{value:g_++}),this.uuid=Ji(),this.data=e,this.dataReady=!0,this.version=0}getSize(e){let t=this.data;return typeof HTMLVideoElement<"u"&&t instanceof HTMLVideoElement?e.set(t.videoWidth,t.videoHeight,0):typeof VideoFrame<"u"&&t instanceof VideoFrame?e.set(t.displayWidth,t.displayHeight,0):t!==null?e.set(t.width,t.height,t.depth||0):e.set(0,0,0),e}set needsUpdate(e){e===!0&&this.version++}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];let i={uuid:this.uuid,url:""},s=this.data;if(s!==null){let r;if(Array.isArray(s)){r=[];for(let o=0,a=s.length;o<a;o++)s[o].isDataTexture?r.push(Bu(s[o].image)):r.push(Bu(s[o]))}else r=Bu(s);i.url=r}return t||(e.images[this.uuid]=i),i}};function Bu(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?Xc.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(nt("Texture: Unable to serialize Texture."),{})}var __=0,Hu=new y,In=class n extends Qi{constructor(e=n.DEFAULT_IMAGE,t=n.DEFAULT_MAPPING,i=Ii,s=Ii,r=yn,o=is,a=Si,c=di,l=n.DEFAULT_ANISOTROPY,u=$s){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:__++}),this.uuid=Ji(),this.name="",this.source=new $o(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=s,this.magFilter=r,this.minFilter=o,this.anisotropy=l,this.format=a,this.internalFormat=null,this.type=c,this.offset=new Pe(0,0),this.repeat=new Pe(1,1),this.center=new Pe(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new gt,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=u,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(e&&e.depth&&e.depth>1),this.pmremVersion=0,this.normalized=!1}get width(){return this.source.getSize(Hu).x}get height(){return this.source.getSize(Hu).y}get depth(){return this.source.getSize(Hu).z}get image(){return this.source.data}set image(e){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.normalized=e.normalized,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.isArrayTexture=e.isArrayTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}setValues(e){for(let t in e){let i=e[t];if(i===void 0){nt(`Texture.setValues(): parameter '${t}' has value of undefined.`);continue}let s=this[t];if(s===void 0){nt(`Texture.setValues(): property '${t}' does not exist.`);continue}s&&i&&s.isVector2&&i.isVector2||s&&i&&s.isVector3&&i.isVector3||s&&i&&s.isMatrix3&&i.isMatrix3?s.copy(i):this[t]=i}}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];let i={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,normalized:this.normalized,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Od)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case oi:e.x=e.x-Math.floor(e.x);break;case Ii:e.x=e.x<0?0:1;break;case Wo:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case oi:e.y=e.y-Math.floor(e.y);break;case Ii:e.y=e.y<0?0:1;break;case Wo:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}};In.DEFAULT_IMAGE=null;In.DEFAULT_MAPPING=Od;In.DEFAULT_ANISOTROPY=1;var $t=class n{static{n.prototype.isVector4=!0}constructor(e=0,t=0,i=0,s=1){this.x=e,this.y=t,this.z=i,this.w=s}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,s){return this.x=e,this.y=t,this.z=i,this.w=s,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("THREE.Vector4: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("THREE.Vector4: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){let t=this.x,i=this.y,s=this.z,r=this.w,o=e.elements;return this.x=o[0]*t+o[4]*i+o[8]*s+o[12]*r,this.y=o[1]*t+o[5]*i+o[9]*s+o[13]*r,this.z=o[2]*t+o[6]*i+o[10]*s+o[14]*r,this.w=o[3]*t+o[7]*i+o[11]*s+o[15]*r,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);let t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,s,r,c=e.elements,l=c[0],u=c[4],d=c[8],f=c[1],p=c[5],x=c[9],b=c[2],g=c[6],m=c[10];if(Math.abs(u-f)<.01&&Math.abs(d-b)<.01&&Math.abs(x-g)<.01){if(Math.abs(u+f)<.1&&Math.abs(d+b)<.1&&Math.abs(x+g)<.1&&Math.abs(l+p+m-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;let U=(l+1)/2,T=(p+1)/2,I=(m+1)/2,L=(u+f)/4,P=(d+b)/4,M=(x+g)/4;return U>T&&U>I?U<.01?(i=0,s=.707106781,r=.707106781):(i=Math.sqrt(U),s=L/i,r=P/i):T>I?T<.01?(i=.707106781,s=0,r=.707106781):(s=Math.sqrt(T),i=L/s,r=M/s):I<.01?(i=.707106781,s=.707106781,r=0):(r=Math.sqrt(I),i=P/r,s=M/r),this.set(i,s,r,t),this}let A=Math.sqrt((g-x)*(g-x)+(d-b)*(d-b)+(f-u)*(f-u));return Math.abs(A)<.001&&(A=1),this.x=(g-x)/A,this.y=(d-b)/A,this.z=(f-u)/A,this.w=Math.acos((l+p+m-1)/2),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=St(this.x,e.x,t.x),this.y=St(this.y,e.y,t.y),this.z=St(this.z,e.z,t.z),this.w=St(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=St(this.x,e,t),this.y=St(this.y,e,t),this.z=St(this.z,e,t),this.w=St(this.w,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(St(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}},qc=class extends Qi{constructor(e=1,t=1,i={}){super(),i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:yn,depthBuffer:!0,stencilBuffer:!1,resolveColorBuffer:!0,resolveDepthBuffer:!0,resolveStencilBuffer:!0,storeMultisampledColorBuffer:!0,storeMultisampledDepthBuffer:!0,storeMultisampledStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1,useArrayDepthTexture:!1},i),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=i.depth,this.scissor=new $t(0,0,e,t),this.scissorTest=!1,this.viewport=new $t(0,0,e,t),this.textures=[];let s={width:e,height:t,depth:i.depth},r=new In(s),o=i.count;for(let a=0;a<o;a++)this.textures[a]=r.clone(),this.textures[a].isRenderTargetTexture=!0,this.textures[a].renderTarget=this;this._setTextureOptions(i),this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveColorBuffer=i.resolveColorBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this.storeMultisampledColorBuffer=i.storeMultisampledColorBuffer,this.storeMultisampledDepthBuffer=i.storeMultisampledDepthBuffer,this.storeMultisampledStencilBuffer=i.storeMultisampledStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples,this.multiview=i.multiview,this.useArrayDepthTexture=i.useArrayDepthTexture}_setTextureOptions(e={}){let t={minFilter:yn,generateMipmaps:!1,flipY:!1,internalFormat:null};e.mapping!==void 0&&(t.mapping=e.mapping),e.wrapS!==void 0&&(t.wrapS=e.wrapS),e.wrapT!==void 0&&(t.wrapT=e.wrapT),e.wrapR!==void 0&&(t.wrapR=e.wrapR),e.magFilter!==void 0&&(t.magFilter=e.magFilter),e.minFilter!==void 0&&(t.minFilter=e.minFilter),e.format!==void 0&&(t.format=e.format),e.type!==void 0&&(t.type=e.type),e.anisotropy!==void 0&&(t.anisotropy=e.anisotropy),e.colorSpace!==void 0&&(t.colorSpace=e.colorSpace),e.flipY!==void 0&&(t.flipY=e.flipY),e.generateMipmaps!==void 0&&(t.generateMipmaps=e.generateMipmaps),e.internalFormat!==void 0&&(t.internalFormat=e.internalFormat);for(let i=0;i<this.textures.length;i++)this.textures[i].setValues(t)}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&this._depthTexture.renderTarget===this&&(this._depthTexture.renderTarget=null),e!==null&&e.renderTarget===null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let s=0,r=this.textures.length;s<r;s++)this.textures[s].image.width=e,this.textures[s].image.height=t,this.textures[s].image.depth=i,this.textures[s].isData3DTexture!==!0&&(this.textures[s].isArrayTexture=this.textures[s].image.depth>1);this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;let s=Object.assign({},e.textures[t].image);this.textures[t].source=new $o(s)}if(this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveColorBuffer=e.resolveColorBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,this.storeMultisampledColorBuffer=e.storeMultisampledColorBuffer,this.storeMultisampledDepthBuffer=e.storeMultisampledDepthBuffer,this.storeMultisampledStencilBuffer=e.storeMultisampledStencilBuffer,e.depthTexture!==null)if(e.depthTexture.renderTarget===e){let t=e.depthTexture.clone();t.renderTarget=null,this.depthTexture=t}else this.depthTexture=e.depthTexture;return this.samples=e.samples,this.multiview=e.multiview,this.useArrayDepthTexture=e.useArrayDepthTexture,this}dispose(){this.dispatchEvent({type:"dispose"})}},ai=class extends qc{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}},Ja=class extends In{constructor(e=null,t=1,i=1,s=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:s},this.magFilter=vn,this.minFilter=vn,this.wrapR=Ii,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}copy(e){return super.copy(e),this.wrapR=e.wrapR,this}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}};var Yc=class extends In{constructor(e=null,t=1,i=1,s=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:s},this.magFilter=vn,this.minFilter=vn,this.wrapR=Ii,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}copy(e){return super.copy(e),this.wrapR=e.wrapR,this}};var rt=class n{static{n.prototype.isMatrix4=!0}constructor(e,t,i,s,r,o,a,c,l,u,d,f,p,x,b,g){this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,s,r,o,a,c,l,u,d,f,p,x,b,g)}set(e,t,i,s,r,o,a,c,l,u,d,f,p,x,b,g){let m=this.elements;return m[0]=e,m[4]=t,m[8]=i,m[12]=s,m[1]=r,m[5]=o,m[9]=a,m[13]=c,m[2]=l,m[6]=u,m[10]=d,m[14]=f,m[3]=p,m[7]=x,m[11]=b,m[15]=g,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new n().fromArray(this.elements)}copy(e){let t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){let t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){let t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return this.determinantAffine()===0?(e.set(1,0,0),t.set(0,1,0),i.set(0,0,1),this):(e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this)}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){if(e.determinantAffine()===0)return this.identity();let t=this.elements,i=e.elements,s=1/To.setFromMatrixColumn(e,0).length(),r=1/To.setFromMatrixColumn(e,1).length(),o=1/To.setFromMatrixColumn(e,2).length();return t[0]=i[0]*s,t[1]=i[1]*s,t[2]=i[2]*s,t[3]=0,t[4]=i[4]*r,t[5]=i[5]*r,t[6]=i[6]*r,t[7]=0,t[8]=i[8]*o,t[9]=i[9]*o,t[10]=i[10]*o,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){let t=this.elements,i=e.x,s=e.y,r=e.z,o=Math.cos(i),a=Math.sin(i),c=Math.cos(s),l=Math.sin(s),u=Math.cos(r),d=Math.sin(r);if(e.order==="XYZ"){let f=o*u,p=o*d,x=a*u,b=a*d;t[0]=c*u,t[4]=-c*d,t[8]=l,t[1]=p+x*l,t[5]=f-b*l,t[9]=-a*c,t[2]=b-f*l,t[6]=x+p*l,t[10]=o*c}else if(e.order==="YXZ"){let f=c*u,p=c*d,x=l*u,b=l*d;t[0]=f+b*a,t[4]=x*a-p,t[8]=o*l,t[1]=o*d,t[5]=o*u,t[9]=-a,t[2]=p*a-x,t[6]=b+f*a,t[10]=o*c}else if(e.order==="ZXY"){let f=c*u,p=c*d,x=l*u,b=l*d;t[0]=f-b*a,t[4]=-o*d,t[8]=x+p*a,t[1]=p+x*a,t[5]=o*u,t[9]=b-f*a,t[2]=-o*l,t[6]=a,t[10]=o*c}else if(e.order==="ZYX"){let f=o*u,p=o*d,x=a*u,b=a*d;t[0]=c*u,t[4]=x*l-p,t[8]=f*l+b,t[1]=c*d,t[5]=b*l+f,t[9]=p*l-x,t[2]=-l,t[6]=a*c,t[10]=o*c}else if(e.order==="YZX"){let f=o*c,p=o*l,x=a*c,b=a*l;t[0]=c*u,t[4]=b-f*d,t[8]=x*d+p,t[1]=d,t[5]=o*u,t[9]=-a*u,t[2]=-l*u,t[6]=p*d+x,t[10]=f-b*d}else if(e.order==="XZY"){let f=o*c,p=o*l,x=a*c,b=a*l;t[0]=c*u,t[4]=-d,t[8]=l*u,t[1]=f*d+b,t[5]=o*u,t[9]=p*d-x,t[2]=x*d-p,t[6]=a*u,t[10]=b*d+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(x_,e,v_)}lookAt(e,t,i){let s=this.elements;return vi.subVectors(e,t),vi.lengthSq()===0&&(vi.z=1),vi.normalize(),ir.crossVectors(i,vi),ir.lengthSq()===0&&(Math.abs(i.z)===1?vi.x+=1e-4:vi.z+=1e-4,vi.normalize(),ir.crossVectors(i,vi)),ir.normalize(),sc.crossVectors(vi,ir),s[0]=ir.x,s[4]=sc.x,s[8]=vi.x,s[1]=ir.y,s[5]=sc.y,s[9]=vi.y,s[2]=ir.z,s[6]=sc.z,s[10]=vi.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let i=e.elements,s=t.elements,r=this.elements,o=i[0],a=i[4],c=i[8],l=i[12],u=i[1],d=i[5],f=i[9],p=i[13],x=i[2],b=i[6],g=i[10],m=i[14],A=i[3],U=i[7],T=i[11],I=i[15],L=s[0],P=s[4],M=s[8],C=s[12],O=s[1],H=s[5],k=s[9],q=s[13],z=s[2],ee=s[6],he=s[10],ue=s[14],ye=s[3],V=s[7],Q=s[11],le=s[15];return r[0]=o*L+a*O+c*z+l*ye,r[4]=o*P+a*H+c*ee+l*V,r[8]=o*M+a*k+c*he+l*Q,r[12]=o*C+a*q+c*ue+l*le,r[1]=u*L+d*O+f*z+p*ye,r[5]=u*P+d*H+f*ee+p*V,r[9]=u*M+d*k+f*he+p*Q,r[13]=u*C+d*q+f*ue+p*le,r[2]=x*L+b*O+g*z+m*ye,r[6]=x*P+b*H+g*ee+m*V,r[10]=x*M+b*k+g*he+m*Q,r[14]=x*C+b*q+g*ue+m*le,r[3]=A*L+U*O+T*z+I*ye,r[7]=A*P+U*H+T*ee+I*V,r[11]=A*M+U*k+T*he+I*Q,r[15]=A*C+U*q+T*ue+I*le,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){let e=this.elements,t=e[0],i=e[4],s=e[8],r=e[12],o=e[1],a=e[5],c=e[9],l=e[13],u=e[2],d=e[6],f=e[10],p=e[14],x=e[3],b=e[7],g=e[11],m=e[15],A=c*p-l*f,U=a*p-l*d,T=a*f-c*d,I=o*p-l*u,L=o*f-c*u,P=o*d-a*u;return t*(b*A-g*U+m*T)-i*(x*A-g*I+m*L)+s*(x*U-b*I+m*P)-r*(x*T-b*L+g*P)}determinantAffine(){let e=this.elements,t=e[0],i=e[4],s=e[8],r=e[1],o=e[5],a=e[9],c=e[2],l=e[6],u=e[10];return t*(o*u-a*l)-i*(r*u-a*c)+s*(r*l-o*c)}transpose(){let e=this.elements,t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){let s=this.elements;return e.isVector3?(s[12]=e.x,s[13]=e.y,s[14]=e.z):(s[12]=e,s[13]=t,s[14]=i),this}invert(){let e=this.elements,t=e[0],i=e[1],s=e[2],r=e[3],o=e[4],a=e[5],c=e[6],l=e[7],u=e[8],d=e[9],f=e[10],p=e[11],x=e[12],b=e[13],g=e[14],m=e[15],A=t*a-i*o,U=t*c-s*o,T=t*l-r*o,I=i*c-s*a,L=i*l-r*a,P=s*l-r*c,M=u*b-d*x,C=u*g-f*x,O=u*m-p*x,H=d*g-f*b,k=d*m-p*b,q=f*m-p*g,z=A*q-U*k+T*H+I*O-L*C+P*M;if(z===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let ee=1/z;return e[0]=(a*q-c*k+l*H)*ee,e[1]=(s*k-i*q-r*H)*ee,e[2]=(b*P-g*L+m*I)*ee,e[3]=(f*L-d*P-p*I)*ee,e[4]=(c*O-o*q-l*C)*ee,e[5]=(t*q-s*O+r*C)*ee,e[6]=(g*T-x*P-m*U)*ee,e[7]=(u*P-f*T+p*U)*ee,e[8]=(o*k-a*O+l*M)*ee,e[9]=(i*O-t*k-r*M)*ee,e[10]=(x*L-b*T+m*A)*ee,e[11]=(d*T-u*L-p*A)*ee,e[12]=(a*C-o*H-c*M)*ee,e[13]=(t*H-i*C+s*M)*ee,e[14]=(b*U-x*I-g*A)*ee,e[15]=(u*I-d*U+f*A)*ee,this}scale(e){let t=this.elements,i=e.x,s=e.y,r=e.z;return t[0]*=i,t[4]*=s,t[8]*=r,t[1]*=i,t[5]*=s,t[9]*=r,t[2]*=i,t[6]*=s,t[10]*=r,t[3]*=i,t[7]*=s,t[11]*=r,this}getMaxScaleOnAxis(){let e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],s=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,s))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){let t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){let i=Math.cos(t),s=Math.sin(t),r=1-i,o=e.x,a=e.y,c=e.z,l=r*o,u=r*a;return this.set(l*o+i,l*a-s*c,l*c+s*a,0,l*a+s*c,u*a+i,u*c-s*o,0,l*c-s*a,u*c+s*o,r*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,s,r,o){return this.set(1,i,r,0,e,1,o,0,t,s,1,0,0,0,0,1),this}compose(e,t,i){let s=this.elements,r=t._x,o=t._y,a=t._z,c=t._w,l=r+r,u=o+o,d=a+a,f=r*l,p=r*u,x=r*d,b=o*u,g=o*d,m=a*d,A=c*l,U=c*u,T=c*d,I=i.x,L=i.y,P=i.z;return s[0]=(1-(b+m))*I,s[1]=(p+T)*I,s[2]=(x-U)*I,s[3]=0,s[4]=(p-T)*L,s[5]=(1-(f+m))*L,s[6]=(g+A)*L,s[7]=0,s[8]=(x+U)*P,s[9]=(g-A)*P,s[10]=(1-(f+b))*P,s[11]=0,s[12]=e.x,s[13]=e.y,s[14]=e.z,s[15]=1,this}decompose(e,t,i){let s=this.elements;e.x=s[12],e.y=s[13],e.z=s[14];let r=this.determinantAffine();if(r===0)return i.set(1,1,1),t.identity(),this;let o=To.set(s[0],s[1],s[2]).length(),a=To.set(s[4],s[5],s[6]).length(),c=To.set(s[8],s[9],s[10]).length();r<0&&(o=-o),Yi.copy(this);let l=1/o,u=1/a,d=1/c;return Yi.elements[0]*=l,Yi.elements[1]*=l,Yi.elements[2]*=l,Yi.elements[4]*=u,Yi.elements[5]*=u,Yi.elements[6]*=u,Yi.elements[8]*=d,Yi.elements[9]*=d,Yi.elements[10]*=d,t.setFromRotationMatrix(Yi),i.x=o,i.y=a,i.z=c,this}makePerspective(e,t,i,s,r,o,a=ji,c=!1){let l=this.elements,u=2*r/(t-e),d=2*r/(i-s),f=(t+e)/(t-e),p=(i+s)/(i-s),x,b;if(c)x=r/(o-r),b=o*r/(o-r);else if(a===ji)x=-(o+r)/(o-r),b=-2*o*r/(o-r);else if(a===Xo)x=-o/(o-r),b=-o*r/(o-r);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+a);return l[0]=u,l[4]=0,l[8]=f,l[12]=0,l[1]=0,l[5]=d,l[9]=p,l[13]=0,l[2]=0,l[6]=0,l[10]=x,l[14]=b,l[3]=0,l[7]=0,l[11]=-1,l[15]=0,this}makeOrthographic(e,t,i,s,r,o,a=ji,c=!1){let l=this.elements,u=2/(t-e),d=2/(i-s),f=-(t+e)/(t-e),p=-(i+s)/(i-s),x,b;if(c)x=1/(o-r),b=o/(o-r);else if(a===ji)x=-2/(o-r),b=-(o+r)/(o-r);else if(a===Xo)x=-1/(o-r),b=-r/(o-r);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+a);return l[0]=u,l[4]=0,l[8]=0,l[12]=f,l[1]=0,l[5]=d,l[9]=0,l[13]=p,l[2]=0,l[6]=0,l[10]=x,l[14]=b,l[3]=0,l[7]=0,l[11]=0,l[15]=1,this}equals(e){let t=this.elements,i=e.elements;for(let s=0;s<16;s++)if(t[s]!==i[s])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){let i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}},To=new y,Yi=new rt,x_=new y(0,0,0),v_=new y(1,1,1),ir=new y,sc=new y,vi=new y,Op=new rt,Bp=new rn,Pi=class n{constructor(e=0,t=0,i=0,s=n.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=s}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,s=this._order){return this._x=e,this._y=t,this._z=i,this._order=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){let s=e.elements,r=s[0],o=s[4],a=s[8],c=s[1],l=s[5],u=s[9],d=s[2],f=s[6],p=s[10];switch(t){case"XYZ":this._y=Math.asin(St(a,-1,1)),Math.abs(a)<.9999999?(this._x=Math.atan2(-u,p),this._z=Math.atan2(-o,r)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-St(u,-1,1)),Math.abs(u)<.9999999?(this._y=Math.atan2(a,p),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-d,r),this._z=0);break;case"ZXY":this._x=Math.asin(St(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-d,p),this._z=Math.atan2(-o,l)):(this._y=0,this._z=Math.atan2(c,r));break;case"ZYX":this._y=Math.asin(-St(d,-1,1)),Math.abs(d)<.9999999?(this._x=Math.atan2(f,p),this._z=Math.atan2(c,r)):(this._x=0,this._z=Math.atan2(-o,l));break;case"YZX":this._z=Math.asin(St(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-u,l),this._y=Math.atan2(-d,r)):(this._x=0,this._y=Math.atan2(a,p));break;case"XZY":this._z=Math.asin(-St(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(a,r)):(this._x=Math.atan2(-u,p),this._y=0);break;default:nt("Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return Op.makeRotationFromQuaternion(e),this.setFromRotationMatrix(Op,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return Bp.setFromEuler(this),this.setFromQuaternion(Bp,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};Pi.DEFAULT_ORDER="XYZ";var Zo=class{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}},y_=0,Hp=new y,So=new rn,Ns=new rt,rc=new y,Fa=new y,M_=new y,E_=new rn,kp=new y(1,0,0),Vp=new y(0,1,0),zp=new y(0,0,1),Gp={type:"added"},b_={type:"removed"},wo={type:"childadded",child:null},ku={type:"childremoved",child:null},an=class n extends Qi{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:y_++}),this.uuid=Ji(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=n.DEFAULT_UP.clone();let e=new y,t=new Pi,i=new rn,s=new y(1,1,1);function r(){i.setFromEuler(t,!1)}function o(){t.setFromQuaternion(i,void 0,!1)}t._onChange(r),i._onChange(o),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:s},modelViewMatrix:{value:new rt},normalMatrix:{value:new gt}}),this.matrix=new rt,this.matrixWorld=new rt,this.matrixAutoUpdate=n.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=n.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Zo,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.static=!1,this.userData={},this.pivot=null}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return So.setFromAxisAngle(e,t),this.quaternion.multiply(So),this}rotateOnWorldAxis(e,t){return So.setFromAxisAngle(e,t),this.quaternion.premultiply(So),this}rotateX(e){return this.rotateOnAxis(kp,e)}rotateY(e){return this.rotateOnAxis(Vp,e)}rotateZ(e){return this.rotateOnAxis(zp,e)}translateOnAxis(e,t){return Hp.copy(e).applyQuaternion(this.quaternion),this.position.add(Hp.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(kp,e)}translateY(e){return this.translateOnAxis(Vp,e)}translateZ(e){return this.translateOnAxis(zp,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(Ns.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?rc.copy(e):rc.set(e,t,i);let s=this.parent;this.updateWorldMatrix(!0,!1),Fa.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?Ns.lookAt(Fa,rc,this.up):Ns.lookAt(rc,Fa,this.up),this.quaternion.setFromRotationMatrix(Ns),s&&(Ns.extractRotation(s.matrixWorld),So.setFromRotationMatrix(Ns),this.quaternion.premultiply(So.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(ht("Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Gp),wo.child=e,this.dispatchEvent(wo),wo.child=null):ht("Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}let t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(b_),ku.child=e,this.dispatchEvent(ku),ku.child=null),this}removeFromParent(){let e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),Ns.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),Ns.multiply(e.parent.matrixWorld)),e.applyMatrix4(Ns),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Gp),wo.child=e,this.dispatchEvent(wo),wo.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,s=this.children.length;i<s;i++){let o=this.children[i].getObjectByProperty(e,t);if(o!==void 0)return o}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);let s=this.children;for(let r=0,o=s.length;r<o;r++)s[r].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Fa,e,M_),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Fa,E_,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);let t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}intersectsFrustum(){}traverse(e){e(this);let t=this.children;for(let i=0,s=t.length;i<s;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);let t=this.children;for(let i=0,s=t.length;i<s;i++)t[i].traverseVisible(e)}traverseAncestors(e){let t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale);let e=this.pivot;if(e!==null){let t=e.x,i=e.y,s=e.z,r=this.matrix.elements;r[12]+=t-r[0]*t-r[4]*i-r[8]*s,r[13]+=i-r[1]*t-r[5]*i-r[9]*s,r[14]+=s-r[2]*t-r[6]*i-r[10]*s}this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);let t=this.children;for(let i=0,s=t.length;i<s;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t,i=!1){let s=this.parent;if(e===!0&&s!==null&&s.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||i)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,i=!0),t===!0){let r=this.children;for(let o=0,a=r.length;o<a;o++)r[o].updateWorldMatrix(!1,!0,i)}}toJSON(e){let t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let s={};s.uuid=this.uuid,s.type=this.type,s.name=this.name,s.castShadow=this.castShadow,s.receiveShadow=this.receiveShadow,s.visible=this.visible,s.frustumCulled=this.frustumCulled,s.renderOrder=this.renderOrder,s.static=this.static,s.matrixAutoUpdate=this.matrixAutoUpdate,Object.keys(this.userData).length>0&&(s.userData=this.userData),s.layers=this.layers.mask,s.matrix=this.matrix.toArray(),s.up=this.up.toArray(),this.pivot!==null&&(s.pivot=this.pivot.toArray()),this.morphTargetDictionary!==void 0&&(s.morphTargetDictionary=Object.assign({},this.morphTargetDictionary)),this.morphTargetInfluences!==void 0&&(s.morphTargetInfluences=this.morphTargetInfluences.slice()),this.isInstancedMesh&&(s.type="InstancedMesh",s.count=this.count,s.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(s.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(s.type="BatchedMesh",s.perObjectFrustumCulled=this.perObjectFrustumCulled,s.sortObjects=this.sortObjects,s.drawRanges=this._drawRanges,s.reservedRanges=this._reservedRanges,s.geometryInfo=this._geometryInfo.map(a=>({...a,boundingBox:a.boundingBox?a.boundingBox.toJSON():void 0,boundingSphere:a.boundingSphere?a.boundingSphere.toJSON():void 0})),s.instanceInfo=this._instanceInfo.map(a=>({...a})),s.availableInstanceIds=this._availableInstanceIds.slice(),s.availableGeometryIds=this._availableGeometryIds.slice(),s.nextIndexStart=this._nextIndexStart,s.nextVertexStart=this._nextVertexStart,s.geometryCount=this._geometryCount,s.maxInstanceCount=this._maxInstanceCount,s.maxVertexCount=this._maxVertexCount,s.maxIndexCount=this._maxIndexCount,s.geometryInitialized=this._geometryInitialized,s.matricesTexture=this._matricesTexture.toJSON(e),s.indirectTexture=this._indirectTexture.toJSON(e),this._colorsTexture!==null&&(s.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(s.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(s.boundingBox=this.boundingBox.toJSON()));function r(a,c){return a[c.uuid]===void 0&&(a[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?s.background=this.background.toJSON():this.background.isTexture&&(s.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(s.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){s.geometry=r(e.geometries,this.geometry);let a=this.geometry.parameters;if(a!==void 0&&a.shapes!==void 0){let c=a.shapes;if(Array.isArray(c))for(let l=0,u=c.length;l<u;l++){let d=c[l];r(e.shapes,d)}else r(e.shapes,c)}}if(this.isSkinnedMesh&&(s.bindMode=this.bindMode,s.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(r(e.skeletons,this.skeleton),s.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let a=[];for(let c=0,l=this.material.length;c<l;c++)a.push(r(e.materials,this.material[c]));s.material=a}else s.material=r(e.materials,this.material);if(this.children.length>0){s.children=[];for(let a=0;a<this.children.length;a++)s.children.push(this.children[a].toJSON(e).object)}if(this.animations.length>0){s.animations=[];for(let a=0;a<this.animations.length;a++){let c=this.animations[a];s.animations.push(r(e.animations,c))}}if(t){let a=o(e.geometries),c=o(e.materials),l=o(e.textures),u=o(e.images),d=o(e.shapes),f=o(e.skeletons),p=o(e.animations),x=o(e.nodes);a.length>0&&(i.geometries=a),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),u.length>0&&(i.images=u),d.length>0&&(i.shapes=d),f.length>0&&(i.skeletons=f),p.length>0&&(i.animations=p),x.length>0&&(i.nodes=x)}return i.object=s,i;function o(a){let c=[];for(let l in a){let u=a[l];delete u.metadata,c.push(u)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.pivot=e.pivot!==null?e.pivot.clone():null,this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.static=e.static,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){let s=e.children[i];this.add(s.clone())}return this}dispose(){this.dispatchEvent({type:"dispose"})}};an.DEFAULT_UP=new y(0,1,0);an.DEFAULT_MATRIX_AUTO_UPDATE=!0;an.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var Oe=class extends an{constructor(){super(),this.isGroup=!0,this.type="Group"}},T_={type:"move"},Ko=class{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new Oe,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new Oe,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new y,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new y),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new Oe,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new y,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new y,this._grip.eventsEnabled=!1),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){let t=this._hand;if(t)for(let i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let s=null,r=null,o=null,a=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){o=!0;for(let b of e.hand.values()){let g=t.getJointPose(b,i),m=this._getHandJoint(l,b);g!==null&&(m.matrix.fromArray(g.transform.matrix),m.matrix.decompose(m.position,m.rotation,m.scale),m.matrixWorldNeedsUpdate=!0,m.jointRadius=g.radius),m.visible=g!==null}let u=l.joints["index-finger-tip"],d=l.joints["thumb-tip"],f=u.position.distanceTo(d.position),p=.02,x=.005;l.inputState.pinching&&f>p+x?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=p-x&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(r=t.getPose(e.gripSpace,i),r!==null&&(c.matrix.fromArray(r.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,r.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(r.linearVelocity)):c.hasLinearVelocity=!1,r.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(r.angularVelocity)):c.hasAngularVelocity=!1,c.eventsEnabled&&c.dispatchEvent({type:"gripUpdated",data:e,target:this})));a!==null&&(s=t.getPose(e.targetRaySpace,i),s===null&&r!==null&&(s=r),s!==null&&(a.matrix.fromArray(s.transform.matrix),a.matrix.decompose(a.position,a.rotation,a.scale),a.matrixWorldNeedsUpdate=!0,s.linearVelocity?(a.hasLinearVelocity=!0,a.linearVelocity.copy(s.linearVelocity)):a.hasLinearVelocity=!1,s.angularVelocity?(a.hasAngularVelocity=!0,a.angularVelocity.copy(s.angularVelocity)):a.hasAngularVelocity=!1,this.dispatchEvent(T_)))}return a!==null&&(a.visible=s!==null),c!==null&&(c.visible=r!==null),l!==null&&(l.visible=o!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){let i=new Oe;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}},r0={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},sr={h:0,s:0,l:0},oc={h:0,s:0,l:0};function Vu(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}var ke=class{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){let s=e;s&&s.isColor?this.copy(s):typeof s=="number"?this.setHex(s):typeof s=="string"&&this.setStyle(s)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=sn){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,It.colorSpaceToWorking(this,t),this}setRGB(e,t,i,s=It.workingColorSpace){return this.r=e,this.g=t,this.b=i,It.colorSpaceToWorking(this,s),this}setHSL(e,t,i,s=It.workingColorSpace){if(e=Yd(e,1),t=St(t,0,1),i=St(i,0,1),t===0)this.r=this.g=this.b=i;else{let r=i<=.5?i*(1+t):i+t-i*t,o=2*i-r;this.r=Vu(o,r,e+1/3),this.g=Vu(o,r,e),this.b=Vu(o,r,e-1/3)}return It.colorSpaceToWorking(this,s),this}setStyle(e,t=sn){function i(r){r!==void 0&&parseFloat(r)<1&&nt("Color: Alpha component of "+e+" will be ignored.")}let s;if(s=/^(\w+)\(([^\)]*)\)/.exec(e)){let r,o=s[1],a=s[2];switch(o){case"rgb":case"rgba":if(r=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(a))return i(r[4]),this.setRGB(Math.min(255,parseInt(r[1],10))/255,Math.min(255,parseInt(r[2],10))/255,Math.min(255,parseInt(r[3],10))/255,t);if(r=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(a))return i(r[4]),this.setRGB(Math.min(100,parseInt(r[1],10))/100,Math.min(100,parseInt(r[2],10))/100,Math.min(100,parseInt(r[3],10))/100,t);break;case"hsl":case"hsla":if(r=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(a))return i(r[4]),this.setHSL(parseFloat(r[1])/360,parseFloat(r[2])/100,parseFloat(r[3])/100,t);break;default:nt("Color: Unknown color model "+e)}}else if(s=/^\#([A-Fa-f\d]+)$/.exec(e)){let r=s[1],o=r.length;if(o===3)return this.setRGB(parseInt(r.charAt(0),16)/15,parseInt(r.charAt(1),16)/15,parseInt(r.charAt(2),16)/15,t);if(o===6)return this.setHex(parseInt(r,16),t);nt("Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=sn){let i=r0[e.toLowerCase()];return i!==void 0?this.setHex(i,t):nt("Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=ks(e.r),this.g=ks(e.g),this.b=ks(e.b),this}copyLinearToSRGB(e){return this.r=zo(e.r),this.g=zo(e.g),this.b=zo(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=sn){return It.workingToColorSpace(Yn.copy(this),e),Math.round(St(Yn.r*255,0,255))*65536+Math.round(St(Yn.g*255,0,255))*256+Math.round(St(Yn.b*255,0,255))}getHexString(e=sn){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=It.workingColorSpace){It.workingToColorSpace(Yn.copy(this),t);let i=Yn.r,s=Yn.g,r=Yn.b,o=Math.max(i,s,r),a=Math.min(i,s,r),c,l,u=(a+o)/2;if(a===o)c=0,l=0;else{let d=o-a;switch(l=u<=.5?d/(o+a):d/(2-o-a),o){case i:c=(s-r)/d+(s<r?6:0);break;case s:c=(r-i)/d+2;break;case r:c=(i-s)/d+4;break}c/=6}return e.h=c,e.s=l,e.l=u,e}getRGB(e,t=It.workingColorSpace){return It.workingToColorSpace(Yn.copy(this),t),e.r=Yn.r,e.g=Yn.g,e.b=Yn.b,e}getStyle(e=sn){It.workingToColorSpace(Yn.copy(this),e);let t=Yn.r,i=Yn.g,s=Yn.b;return e!==sn?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${s.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(s*255)})`}offsetHSL(e,t,i){return this.getHSL(sr),this.setHSL(sr.h+e,sr.s+t,sr.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(sr),e.getHSL(oc);let i=Ya(sr.h,oc.h,t),s=Ya(sr.s,oc.s,t),r=Ya(sr.l,oc.l,t);return this.setHSL(i,s,r),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){let t=this.r,i=this.g,s=this.b,r=e.elements;return this.r=r[0]*t+r[3]*i+r[6]*s,this.g=r[1]*t+r[4]*i+r[7]*s,this.b=r[2]*t+r[5]*i+r[8]*s,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},Yn=new ke;ke.NAMES=r0;var Wr=class n{constructor(e,t=25e-5){this.isFogExp2=!0,this.name="",this.color=new ke(e),this.density=t}clone(){return new n(this.color,this.density)}toJSON(){return{type:"FogExp2",name:this.name,color:this.color.getHex(),density:this.density}}};var jo=class extends an{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Pi,this.environmentIntensity=1,this.environmentRotation=new Pi,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){let t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),t.object.backgroundBlurriness=this.backgroundBlurriness,t.object.backgroundIntensity=this.backgroundIntensity,t.object.backgroundRotation=this.backgroundRotation.toArray(),t.object.environmentIntensity=this.environmentIntensity,t.object.environmentRotation=this.environmentRotation.toArray(),t}},$i=new y,Us=new y,zu=new y,Fs=new y,Ao=new y,Ro=new y,Wp=new y,Gu=new y,Wu=new y,Xu=new y,qu=new $t,Yu=new $t,$u=new $t,gs=class n{constructor(e=new y,t=new y,i=new y){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,s){s.subVectors(i,t),$i.subVectors(e,t),s.cross($i);let r=s.lengthSq();return r>0?s.multiplyScalar(1/Math.sqrt(r)):s.set(0,0,0)}static getBarycoord(e,t,i,s,r){$i.subVectors(s,t),Us.subVectors(i,t),zu.subVectors(e,t);let o=$i.dot($i),a=$i.dot(Us),c=$i.dot(zu),l=Us.dot(Us),u=Us.dot(zu),d=o*l-a*a;if(d===0)return r.set(0,0,0),null;let f=1/d,p=(l*c-a*u)*f,x=(o*u-a*c)*f;return r.set(1-p-x,x,p)}static containsPoint(e,t,i,s){return this.getBarycoord(e,t,i,s,Fs)===null?!1:Fs.x>=0&&Fs.y>=0&&Fs.x+Fs.y<=1}static getInterpolation(e,t,i,s,r,o,a,c){return this.getBarycoord(e,t,i,s,Fs)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(r,Fs.x),c.addScaledVector(o,Fs.y),c.addScaledVector(a,Fs.z),c)}static getInterpolatedAttribute(e,t,i,s,r,o){return qu.setScalar(0),Yu.setScalar(0),$u.setScalar(0),qu.fromBufferAttribute(e,t),Yu.fromBufferAttribute(e,i),$u.fromBufferAttribute(e,s),o.setScalar(0),o.addScaledVector(qu,r.x),o.addScaledVector(Yu,r.y),o.addScaledVector($u,r.z),o}static isFrontFacing(e,t,i,s){return $i.subVectors(i,t),Us.subVectors(e,t),$i.cross(Us).dot(s)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,s){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[s]),this}setFromAttributeAndIndices(e,t,i,s){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,s),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return $i.subVectors(this.c,this.b),Us.subVectors(this.a,this.b),$i.cross(Us).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return n.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return n.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,s,r){return n.getInterpolation(e,this.a,this.b,this.c,t,i,s,r)}containsPoint(e){return n.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return n.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){let i=this.a,s=this.b,r=this.c,o,a;Ao.subVectors(s,i),Ro.subVectors(r,i),Gu.subVectors(e,i);let c=Ao.dot(Gu),l=Ro.dot(Gu);if(c<=0&&l<=0)return t.copy(i);Wu.subVectors(e,s);let u=Ao.dot(Wu),d=Ro.dot(Wu);if(u>=0&&d<=u)return t.copy(s);let f=c*d-u*l;if(f<=0&&c>=0&&u<=0)return o=c/(c-u),t.copy(i).addScaledVector(Ao,o);Xu.subVectors(e,r);let p=Ao.dot(Xu),x=Ro.dot(Xu);if(x>=0&&p<=x)return t.copy(r);let b=p*l-c*x;if(b<=0&&l>=0&&x<=0)return a=l/(l-x),t.copy(i).addScaledVector(Ro,a);let g=u*x-p*d;if(g<=0&&d-u>=0&&p-x>=0)return Wp.subVectors(r,s),a=(d-u)/(d-u+(p-x)),t.copy(s).addScaledVector(Wp,a);let m=1/(g+b+f);return o=b*m,a=f*m,t.copy(i).addScaledVector(Ao,o).addScaledVector(Ro,a)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}},un=class{constructor(e=new y(1/0,1/0,1/0),t=new y(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Zi.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Zi.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){let i=Zi.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);let i=e.geometry;if(i!==void 0){let r=i.getAttribute("position");if(t===!0&&r!==void 0&&e.isInstancedMesh!==!0)for(let o=0,a=r.count;o<a;o++)e.isMesh===!0?e.getVertexPosition(o,Zi):Zi.fromBufferAttribute(r,o),Zi.applyMatrix4(e.matrixWorld),this.expandByPoint(Zi);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),ac.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),ac.copy(i.boundingBox)),ac.applyMatrix4(e.matrixWorld),this.union(ac)}let s=e.children;for(let r=0,o=s.length;r<o;r++)this.expandByObject(s[r],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Zi),Zi.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Oa),lc.subVectors(this.max,Oa),Co.subVectors(e.a,Oa),Io.subVectors(e.b,Oa),Po.subVectors(e.c,Oa),rr.subVectors(Io,Co),or.subVectors(Po,Io),Fr.subVectors(Co,Po);let t=[0,-rr.z,rr.y,0,-or.z,or.y,0,-Fr.z,Fr.y,rr.z,0,-rr.x,or.z,0,-or.x,Fr.z,0,-Fr.x,-rr.y,rr.x,0,-or.y,or.x,0,-Fr.y,Fr.x,0];return!Zu(t,Co,Io,Po,lc)||(t=[1,0,0,0,1,0,0,0,1],!Zu(t,Co,Io,Po,lc))?!1:(cc.crossVectors(rr,or),t=[cc.x,cc.y,cc.z],Zu(t,Co,Io,Po,lc))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Zi).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Zi).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(Os[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),Os[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),Os[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),Os[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),Os[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),Os[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),Os[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),Os[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(Os),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(e){return this.min.fromArray(e.min),this.max.fromArray(e.max),this}},Os=[new y,new y,new y,new y,new y,new y,new y,new y],Zi=new y,ac=new un,Co=new y,Io=new y,Po=new y,rr=new y,or=new y,Fr=new y,Oa=new y,lc=new y,cc=new y,Or=new y;function Zu(n,e,t,i,s){for(let r=0,o=n.length-3;r<=o;r+=3){Or.fromArray(n,r);let a=s.x*Math.abs(Or.x)+s.y*Math.abs(Or.y)+s.z*Math.abs(Or.z),c=e.dot(Or),l=t.dot(Or),u=i.dot(Or);if(Math.max(-Math.max(c,l,u),Math.min(c,l,u))>a)return!1}return!0}var wn=new y,hc=new Pe,S_=0,Cn=class extends Qi{constructor(e,t,i=!1){if(super(),Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:S_++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=Xd,this.updateRanges=[],this.gpuType=Ti,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let s=0,r=this.itemSize;s<r;s++)this.array[e+s]=t.array[i+s];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)hc.fromBufferAttribute(this,t),hc.applyMatrix3(e),this.setXY(t,hc.x,hc.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)wn.fromBufferAttribute(this,t),wn.applyMatrix3(e),this.setXYZ(t,wn.x,wn.y,wn.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)wn.fromBufferAttribute(this,t),wn.applyMatrix4(e),this.setXYZ(t,wn.x,wn.y,wn.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)wn.fromBufferAttribute(this,t),wn.applyNormalMatrix(e),this.setXYZ(t,wn.x,wn.y,wn.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)wn.fromBufferAttribute(this,t),wn.transformDirection(e),this.setXYZ(t,wn.x,wn.y,wn.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Ki(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Yt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Ki(t,this.array)),t}setX(e,t){return this.normalized&&(t=Yt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Ki(t,this.array)),t}setY(e,t){return this.normalized&&(t=Yt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Ki(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Yt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Ki(t,this.array)),t}setW(e,t){return this.normalized&&(t=Yt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,s){return e*=this.itemSize,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array),s=Yt(s,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=s,this}setXYZW(e,t,i,s,r){return e*=this.itemSize,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array),s=Yt(s,this.array),r=Yt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=s,this.array[e+3]=r,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return e.name=this.name,e.usage=this.usage,e.gpuType=this.gpuType,e}dispose(){this.dispatchEvent({type:"dispose"})}};var Qa=class extends Cn{constructor(e,t,i){super(new Uint16Array(e),t,i)}};var el=class extends Cn{constructor(e,t,i){super(new Uint32Array(e),t,i)}};var Dt=class extends Cn{constructor(e,t,i){super(new Float32Array(e),t,i)}},w_=new un,Ba=new y,Ku=new y,li=class{constructor(e=new y,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){let i=this.center;t!==void 0?i.copy(t):w_.setFromPoints(e).getCenter(i);let s=0;for(let r=0,o=e.length;r<o;r++)s=Math.max(s,i.distanceToSquared(e[r]));return this.radius=Math.sqrt(s),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){let t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){let i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Ba.subVectors(e,this.center);let t=Ba.lengthSq();if(t>this.radius*this.radius){let i=Math.sqrt(t),s=(i-this.radius)*.5;this.center.addScaledVector(Ba,s/i),this.radius+=s}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(Ku.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Ba.copy(e.center).add(Ku)),this.expandByPoint(Ba.copy(e.center).sub(Ku))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(e){return this.radius=e.radius,this.center.fromArray(e.center),this}},A_=0,Ci=new rt,ju=new an,Lo=new y,yi=new un,Ha=new un,Nn=new y,tn=class n extends Qi{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:A_++}),this.uuid=Ji(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.indirectOffset=0,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={},this._transformed=!1}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(jg(e)?el:Qa)(e,1):this.index=e,this}setIndirect(e,t=0){return this.indirect=e,this.indirectOffset=t,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){let t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);let i=this.attributes.normal;if(i!==void 0){let r=new gt().getNormalMatrix(e);i.applyNormalMatrix(r),i.needsUpdate=!0}let s=this.attributes.tangent;return s!==void 0&&(s.transformDirection(e),s.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this._transformed=!0,this}applyQuaternion(e){return Ci.makeRotationFromQuaternion(e),this.applyMatrix4(Ci),this}rotateX(e){return Ci.makeRotationX(e),this.applyMatrix4(Ci),this}rotateY(e){return Ci.makeRotationY(e),this.applyMatrix4(Ci),this}rotateZ(e){return Ci.makeRotationZ(e),this.applyMatrix4(Ci),this}translate(e,t,i){return Ci.makeTranslation(e,t,i),this.applyMatrix4(Ci),this}scale(e,t,i){return Ci.makeScale(e,t,i),this.applyMatrix4(Ci),this}lookAt(e){return ju.lookAt(e),ju.updateMatrix(),this.applyMatrix4(ju.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Lo).negate(),this.translate(Lo.x,Lo.y,Lo.z),this}setFromPoints(e){let t=this.getAttribute("position");if(t===void 0){let i=[];for(let s=0,r=e.length;s<r;s++){let o=e[s];i.push(o.x,o.y,o.z||0)}this.setAttribute("position",new Dt(i,3))}else{let i=Math.min(e.length,t.count);for(let s=0;s<i;s++){let r=e[s];t.setXYZ(s,r.x,r.y,r.z||0)}e.length>t.count&&nt("BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new un);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){ht("BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new y(-1/0,-1/0,-1/0),new y(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,s=t.length;i<s;i++){let r=t[i];yi.setFromBufferAttribute(r),this.morphTargetsRelative?(Nn.addVectors(this.boundingBox.min,yi.min),this.boundingBox.expandByPoint(Nn),Nn.addVectors(this.boundingBox.max,yi.max),this.boundingBox.expandByPoint(Nn)):(this.boundingBox.expandByPoint(yi.min),this.boundingBox.expandByPoint(yi.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&ht('BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new li);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){ht("BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new y,1/0);return}if(e){let i=this.boundingSphere.center;if(yi.setFromBufferAttribute(e),t)for(let r=0,o=t.length;r<o;r++){let a=t[r];Ha.setFromBufferAttribute(a),this.morphTargetsRelative?(Nn.addVectors(yi.min,Ha.min),yi.expandByPoint(Nn),Nn.addVectors(yi.max,Ha.max),yi.expandByPoint(Nn)):(yi.expandByPoint(Ha.min),yi.expandByPoint(Ha.max))}yi.getCenter(i);let s=0;for(let r=0,o=e.count;r<o;r++)Nn.fromBufferAttribute(e,r),s=Math.max(s,i.distanceToSquared(Nn));if(t)for(let r=0,o=t.length;r<o;r++){let a=t[r],c=this.morphTargetsRelative;for(let l=0,u=a.count;l<u;l++)Nn.fromBufferAttribute(a,l),c&&(Lo.fromBufferAttribute(e,l),Nn.add(Lo)),s=Math.max(s,i.distanceToSquared(Nn))}this.boundingSphere.radius=Math.sqrt(s),isNaN(this.boundingSphere.radius)&&ht('BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){ht("BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let i=t.position,s=t.normal,r=t.uv,o=this.getAttribute("tangent");(o===void 0||o.count!==i.count)&&(o=new Cn(new Float32Array(4*i.count),4),this.setAttribute("tangent",o));let a=[],c=[];for(let M=0;M<i.count;M++)a[M]=new y,c[M]=new y;let l=new y,u=new y,d=new y,f=new Pe,p=new Pe,x=new Pe,b=new y,g=new y;function m(M,C,O){l.fromBufferAttribute(i,M),u.fromBufferAttribute(i,C),d.fromBufferAttribute(i,O),f.fromBufferAttribute(r,M),p.fromBufferAttribute(r,C),x.fromBufferAttribute(r,O),u.sub(l),d.sub(l),p.sub(f),x.sub(f);let H=1/(p.x*x.y-x.x*p.y);isFinite(H)&&(b.copy(u).multiplyScalar(x.y).addScaledVector(d,-p.y).multiplyScalar(H),g.copy(d).multiplyScalar(p.x).addScaledVector(u,-x.x).multiplyScalar(H),a[M].add(b),a[C].add(b),a[O].add(b),c[M].add(g),c[C].add(g),c[O].add(g))}let A=this.groups;A.length===0&&(A=[{start:0,count:e.count}]);for(let M=0,C=A.length;M<C;++M){let O=A[M],H=O.start,k=O.count;for(let q=H,z=H+k;q<z;q+=3)m(e.getX(q+0),e.getX(q+1),e.getX(q+2))}let U=new y,T=new y,I=new y,L=new y;function P(M){I.fromBufferAttribute(s,M),L.copy(I);let C=a[M];U.copy(C),U.sub(I.multiplyScalar(I.dot(C))).normalize(),T.crossVectors(L,C);let H=T.dot(c[M])<0?-1:1;o.setXYZW(M,U.x,U.y,U.z,H)}for(let M=0,C=A.length;M<C;++M){let O=A[M],H=O.start,k=O.count;for(let q=H,z=H+k;q<z;q+=3)P(e.getX(q+0)),P(e.getX(q+1)),P(e.getX(q+2))}this._transformed=!0}computeVertexNormals(){let e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0||i.count!==t.count)i=new Cn(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,p=i.count;f<p;f++)i.setXYZ(f,0,0,0);let s=new y,r=new y,o=new y,a=new y,c=new y,l=new y,u=new y,d=new y;if(e)for(let f=0,p=e.count;f<p;f+=3){let x=e.getX(f+0),b=e.getX(f+1),g=e.getX(f+2);s.fromBufferAttribute(t,x),r.fromBufferAttribute(t,b),o.fromBufferAttribute(t,g),u.subVectors(o,r),d.subVectors(s,r),u.cross(d),a.fromBufferAttribute(i,x),c.fromBufferAttribute(i,b),l.fromBufferAttribute(i,g),a.add(u),c.add(u),l.add(u),i.setXYZ(x,a.x,a.y,a.z),i.setXYZ(b,c.x,c.y,c.z),i.setXYZ(g,l.x,l.y,l.z)}else for(let f=0,p=t.count;f<p;f+=3)s.fromBufferAttribute(t,f+0),r.fromBufferAttribute(t,f+1),o.fromBufferAttribute(t,f+2),u.subVectors(o,r),d.subVectors(s,r),u.cross(d),i.setXYZ(f+0,u.x,u.y,u.z),i.setXYZ(f+1,u.x,u.y,u.z),i.setXYZ(f+2,u.x,u.y,u.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){let e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)Nn.fromBufferAttribute(e,t),Nn.normalize(),e.setXYZ(t,Nn.x,Nn.y,Nn.z)}toNonIndexed(){function e(a,c){let l=a.array,u=a.itemSize,d=a.normalized,f=new l.constructor(c.length*u),p=0,x=0;for(let b=0,g=c.length;b<g;b++){a.isInterleavedBufferAttribute?p=c[b]*a.data.stride+a.offset:p=c[b]*u;for(let m=0;m<u;m++)f[x++]=l[p++]}return new Cn(f,u,d)}if(this.index===null)return nt("BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let t=new n,i=this.index.array,s=this.attributes;for(let a in s){let c=s[a],l=e(c,i);t.setAttribute(a,l)}let r=this.morphAttributes;for(let a in r){let c=[],l=r[a];for(let u=0,d=l.length;u<d;u++){let f=l[u],p=e(f,i);c.push(p)}t.morphAttributes[a]=c}t.morphTargetsRelative=this.morphTargetsRelative;let o=this.groups;for(let a=0,c=o.length;a<c;a++){let l=o[a];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){let e={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.parameters!==void 0&&this._transformed===!0?"BufferGeometry":this.type,e.name=this.name,Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0&&this._transformed!==!0){let c=this.parameters;for(let l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};let t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});let i=this.attributes;for(let c in i){let l=i[c];e.data.attributes[c]=l.toJSON(e.data)}let s={},r=!1;for(let c in this.morphAttributes){let l=this.morphAttributes[c],u=[];for(let d=0,f=l.length;d<f;d++){let p=l[d];u.push(p.toJSON(e.data))}u.length>0&&(s[c]=u,r=!0)}r&&(e.data.morphAttributes=s,e.data.morphTargetsRelative=this.morphTargetsRelative);let o=this.groups;o.length>0&&(e.data.groups=JSON.parse(JSON.stringify(o)));let a=this.boundingSphere;return a!==null&&(e.data.boundingSphere=a.toJSON()),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let t={};this.name=e.name;let i=e.index;i!==null&&this.setIndex(i.clone());let s=e.attributes;for(let l in s){let u=s[l];this.setAttribute(l,u.clone(t))}let r=e.morphAttributes;for(let l in r){let u=[],d=r[l];for(let f=0,p=d.length;f<p;f++)u.push(d[f].clone(t));this.morphAttributes[l]=u}this.morphTargetsRelative=e.morphTargetsRelative;let o=e.groups;for(let l=0,u=o.length;l<u;l++){let d=o[l];this.addGroup(d.start,d.count,d.materialIndex)}let a=e.boundingBox;a!==null&&(this.boundingBox=a.clone());let c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this._transformed=e._transformed,this}dispose(){this.dispatchEvent({type:"dispose"})}},Xr=class{constructor(e,t){this.isInterleavedBuffer=!0,this.array=e,this.stride=t,this.count=e!==void 0?e.length/t:0,this.usage=Xd,this.updateRanges=[],this.version=0,this.uuid=Ji()}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.array=new e.array.constructor(e.array),this.count=e.count,this.stride=e.stride,this.usage=e.usage,this}copyAt(e,t,i){e*=this.stride,i*=t.stride;for(let s=0,r=this.stride;s<r;s++)this.array[e+s]=t.array[i+s];return this}set(e,t=0){return this.array.set(e,t),this}clone(e){e.arrayBuffers===void 0&&(e.arrayBuffers={}),this.array.buffer._uuid===void 0&&(this.array.buffer._uuid=Ji()),e.arrayBuffers[this.array.buffer._uuid]===void 0&&(e.arrayBuffers[this.array.buffer._uuid]=this.array.slice(0).buffer);let t=new this.array.constructor(e.arrayBuffers[this.array.buffer._uuid]),i=new this.constructor(t,this.stride);return i.setUsage(this.usage),i}onUpload(e){return this.onUploadCallback=e,this}toJSON(e){e.arrayBuffers===void 0&&(e.arrayBuffers={}),this.array.buffer._uuid===void 0&&(this.array.buffer._uuid=Ji()),e.arrayBuffers[this.array.buffer._uuid]===void 0&&(e.arrayBuffers[this.array.buffer._uuid]=Array.from(new Uint32Array(this.array.buffer)));let t={uuid:this.uuid,buffer:this.array.buffer._uuid,type:this.array.constructor.name,stride:this.stride};return t.usage=this.usage,t}},ei=new y,cr=class n{constructor(e,t,i,s=!1){this.isInterleavedBufferAttribute=!0,this.name="",this.data=e,this.itemSize=t,this.offset=i,this.normalized=s}get count(){return this.data.count}get array(){return this.data.array}set needsUpdate(e){this.data.needsUpdate=e}applyMatrix4(e){for(let t=0,i=this.data.count;t<i;t++)ei.fromBufferAttribute(this,t),ei.applyMatrix4(e),this.setXYZ(t,ei.x,ei.y,ei.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)ei.fromBufferAttribute(this,t),ei.applyNormalMatrix(e),this.setXYZ(t,ei.x,ei.y,ei.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)ei.fromBufferAttribute(this,t),ei.transformDirection(e),this.setXYZ(t,ei.x,ei.y,ei.z);return this}getComponent(e,t){let i=this.array[e*this.data.stride+this.offset+t];return this.normalized&&(i=Ki(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Yt(i,this.array)),this.data.array[e*this.data.stride+this.offset+t]=i,this}setX(e,t){return this.normalized&&(t=Yt(t,this.array)),this.data.array[e*this.data.stride+this.offset]=t,this}setY(e,t){return this.normalized&&(t=Yt(t,this.array)),this.data.array[e*this.data.stride+this.offset+1]=t,this}setZ(e,t){return this.normalized&&(t=Yt(t,this.array)),this.data.array[e*this.data.stride+this.offset+2]=t,this}setW(e,t){return this.normalized&&(t=Yt(t,this.array)),this.data.array[e*this.data.stride+this.offset+3]=t,this}getX(e){let t=this.data.array[e*this.data.stride+this.offset];return this.normalized&&(t=Ki(t,this.array)),t}getY(e){let t=this.data.array[e*this.data.stride+this.offset+1];return this.normalized&&(t=Ki(t,this.array)),t}getZ(e){let t=this.data.array[e*this.data.stride+this.offset+2];return this.normalized&&(t=Ki(t,this.array)),t}getW(e){let t=this.data.array[e*this.data.stride+this.offset+3];return this.normalized&&(t=Ki(t,this.array)),t}setXY(e,t,i){return e=e*this.data.stride+this.offset,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=i,this}setXYZ(e,t,i,s){return e=e*this.data.stride+this.offset,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array),s=Yt(s,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=i,this.data.array[e+2]=s,this}setXYZW(e,t,i,s,r){return e=e*this.data.stride+this.offset,this.normalized&&(t=Yt(t,this.array),i=Yt(i,this.array),s=Yt(s,this.array),r=Yt(r,this.array)),this.data.array[e+0]=t,this.data.array[e+1]=i,this.data.array[e+2]=s,this.data.array[e+3]=r,this}clone(e){if(e===void 0){ja("InterleavedBufferAttribute.clone(): Cloning an interleaved buffer attribute will de-interleave buffer data.");let t=[];for(let i=0;i<this.count;i++){let s=i*this.data.stride+this.offset;for(let r=0;r<this.itemSize;r++)t.push(this.data.array[s+r])}return new Cn(new this.array.constructor(t),this.itemSize,this.normalized)}else return e.interleavedBuffers===void 0&&(e.interleavedBuffers={}),e.interleavedBuffers[this.data.uuid]===void 0&&(e.interleavedBuffers[this.data.uuid]=this.data.clone(e)),new n(e.interleavedBuffers[this.data.uuid],this.itemSize,this.offset,this.normalized)}toJSON(e){if(e===void 0){ja("InterleavedBufferAttribute.toJSON(): Serializing an interleaved buffer attribute will de-interleave buffer data.");let t=[];for(let i=0;i<this.count;i++){let s=i*this.data.stride+this.offset;for(let r=0;r<this.itemSize;r++)t.push(this.data.array[s+r])}return{itemSize:this.itemSize,type:this.array.constructor.name,array:t,normalized:this.normalized}}else return e.interleavedBuffers===void 0&&(e.interleavedBuffers={}),e.interleavedBuffers[this.data.uuid]===void 0&&(e.interleavedBuffers[this.data.uuid]=this.data.toJSON(e)),{isInterleavedBufferAttribute:!0,itemSize:this.itemSize,data:this.data.uuid,offset:this.offset,normalized:this.normalized}}},Ju=new y,R_=new y,C_=new gt,Bn=class{constructor(e=new y(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,s){return this.normal.set(e,t,i),this.constant=s,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){let s=Ju.subVectors(i,t).cross(R_.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(s,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){let e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t,i=!0){let s=e.delta(Ju),r=this.normal.dot(s);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;let o=-(e.start.dot(this.normal)+this.constant)/r;return i===!0&&(o<0||o>1)?null:t.copy(e.start).addScaledVector(s,o)}intersectsLine(e){let t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){let i=t||C_.getNormalMatrix(e),s=this.coplanarPoint(Ju).applyMatrix4(e),r=this.normal.applyMatrix3(i).normalize();return this.constant=-s.dot(r),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}toJSON(){return{normal:this.normal.toArray(),constant:this.constant}}fromJSON(e){return this.normal.fromArray(e.normal),this.constant=e.constant,this}},I_=0,ni=class extends Qi{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:I_++}),this.uuid=Ji(),this.name="",this.type="Material",this.blending=Ui,this.side=Es,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Rd,this.blendDst=Cd,this.blendEquation=eo,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ke(0,0,0),this.blendAlpha=0,this.depthFunc=Go,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=$m,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Fc,this.stencilZFail=Fc,this.stencilZPass=Fc,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(let t in e){let i=e[t];if(i===void 0){nt(`Material: parameter '${t}' has value of undefined.`);continue}let s=this[t];if(s===void 0){nt(`Material: '${t}' is not a property of THREE.${this.type}.`);continue}s&&s.isColor?s.set(i):s&&s.isVector2&&i&&i.isVector2||s&&s.isEuler&&i&&i.isEuler||s&&s.isVector3&&i&&i.isVector3?s.copy(i):this[t]=i}}toJSON(e){let t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});let i={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,i.blending=this.blending,i.side=this.side,i.shadowSide=this.shadowSide,i.vertexColors=this.vertexColors,i.opacity=this.opacity,i.transparent=this.transparent,i.blendSrc=this.blendSrc,i.blendDst=this.blendDst,i.blendEquation=this.blendEquation,i.blendSrcAlpha=this.blendSrcAlpha,i.blendDstAlpha=this.blendDstAlpha,i.blendEquationAlpha=this.blendEquationAlpha,i.blendColor=this.blendColor.getHex(),i.blendAlpha=this.blendAlpha,i.depthFunc=this.depthFunc,i.depthTest=this.depthTest,i.depthWrite=this.depthWrite,i.colorWrite=this.colorWrite,i.clipIntersection=this.clipIntersection,i.clipShadows=this.clipShadows,i.stencilWriteMask=this.stencilWriteMask,i.stencilFunc=this.stencilFunc,i.stencilRef=this.stencilRef,i.stencilFuncMask=this.stencilFuncMask,i.stencilFail=this.stencilFail,i.stencilZFail=this.stencilZFail,i.stencilZPass=this.stencilZPass,i.stencilWrite=this.stencilWrite,i.polygonOffset=this.polygonOffset,i.polygonOffsetFactor=this.polygonOffsetFactor,i.polygonOffsetUnits=this.polygonOffsetUnits,i.dithering=this.dithering,i.alphaTest=this.alphaTest,i.alphaHash=this.alphaHash,i.alphaToCoverage=this.alphaToCoverage,i.premultipliedAlpha=this.premultipliedAlpha,i.forceSinglePass=this.forceSinglePass,i.allowOverride=this.allowOverride,i.visible=this.visible,i.toneMapped=this.toneMapped,i.name=this.name,this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.sheenColorMap&&this.sheenColorMap.isTexture&&(i.sheenColorMap=this.sheenColorMap.toJSON(e).uuid),this.sheenRoughnessMap&&this.sheenRoughnessMap.isTexture&&(i.sheenRoughnessMap=this.sheenRoughnessMap.toJSON(e).uuid),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.retroreflectivity!==void 0&&(i.retroreflectivity=this.retroreflectivity),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),Array.isArray(this.clippingPlanes)&&this.clippingPlanes.length>0&&(i.clippingPlanes=this.clippingPlanes.map(r=>r.toJSON())),this.rotation!==void 0&&(i.rotation=this.rotation),this.depthPacking!==void 0&&(i.depthPacking=this.depthPacking),this.linewidth!==void 0&&(i.linewidth=this.linewidth),this.linecap!==void 0&&(i.linecap=this.linecap),this.linejoin!==void 0&&(i.linejoin=this.linejoin),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.wireframe!==void 0&&(i.wireframe=this.wireframe),this.wireframeLinewidth!==void 0&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!==void 0&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!==void 0&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading!==void 0&&(i.flatShading=this.flatShading),this.fog!==void 0&&(i.fog=this.fog),Object.keys(this.userData).length>0&&(i.userData=this.userData);function s(r){let o=[];for(let a in r){let c=r[a];delete c.metadata,o.push(c)}return o}if(t){let r=s(e.textures),o=s(e.images);r.length>0&&(i.textures=r),o.length>0&&(i.images=o)}return i}fromJSON(e,t){if(e.uuid!==void 0&&(this.uuid=e.uuid),e.name!==void 0&&(this.name=e.name),e.color!==void 0&&this.color!==void 0&&this.color.setHex(e.color),e.roughness!==void 0&&(this.roughness=e.roughness),e.metalness!==void 0&&(this.metalness=e.metalness),e.sheen!==void 0&&(this.sheen=e.sheen),e.sheenColor!==void 0&&(this.sheenColor=new ke().setHex(e.sheenColor)),e.sheenRoughness!==void 0&&(this.sheenRoughness=e.sheenRoughness),e.emissive!==void 0&&this.emissive!==void 0&&this.emissive.setHex(e.emissive),e.specular!==void 0&&this.specular!==void 0&&this.specular.setHex(e.specular),e.specularIntensity!==void 0&&(this.specularIntensity=e.specularIntensity),e.specularColor!==void 0&&this.specularColor!==void 0&&this.specularColor.setHex(e.specularColor),e.shininess!==void 0&&(this.shininess=e.shininess),e.clearcoat!==void 0&&(this.clearcoat=e.clearcoat),e.clearcoatRoughness!==void 0&&(this.clearcoatRoughness=e.clearcoatRoughness),e.dispersion!==void 0&&(this.dispersion=e.dispersion),e.retroreflectivity!==void 0&&(this.retroreflectivity=e.retroreflectivity),e.iridescence!==void 0&&(this.iridescence=e.iridescence),e.iridescenceIOR!==void 0&&(this.iridescenceIOR=e.iridescenceIOR),e.iridescenceThicknessRange!==void 0&&(this.iridescenceThicknessRange=e.iridescenceThicknessRange),e.transmission!==void 0&&(this.transmission=e.transmission),e.thickness!==void 0&&(this.thickness=e.thickness),e.attenuationDistance!==void 0&&(this.attenuationDistance=e.attenuationDistance),e.attenuationColor!==void 0&&this.attenuationColor!==void 0&&this.attenuationColor.setHex(e.attenuationColor),e.anisotropy!==void 0&&(this.anisotropy=e.anisotropy),e.anisotropyRotation!==void 0&&(this.anisotropyRotation=e.anisotropyRotation),e.fog!==void 0&&(this.fog=e.fog),e.flatShading!==void 0&&(this.flatShading=e.flatShading),e.blending!==void 0&&(this.blending=e.blending),e.combine!==void 0&&(this.combine=e.combine),e.side!==void 0&&(this.side=e.side),e.shadowSide!==void 0&&(this.shadowSide=e.shadowSide),e.opacity!==void 0&&(this.opacity=e.opacity),e.transparent!==void 0&&(this.transparent=e.transparent),e.alphaTest!==void 0&&(this.alphaTest=e.alphaTest),e.alphaHash!==void 0&&(this.alphaHash=e.alphaHash),e.depthFunc!==void 0&&(this.depthFunc=e.depthFunc),e.depthTest!==void 0&&(this.depthTest=e.depthTest),e.depthWrite!==void 0&&(this.depthWrite=e.depthWrite),e.colorWrite!==void 0&&(this.colorWrite=e.colorWrite),e.clippingPlanes!==void 0&&(this.clippingPlanes=e.clippingPlanes.map(i=>new Bn().fromJSON(i))),e.clipIntersection!==void 0&&(this.clipIntersection=e.clipIntersection),e.clipShadows!==void 0&&(this.clipShadows=e.clipShadows),e.depthPacking!==void 0&&(this.depthPacking=e.depthPacking),e.blendSrc!==void 0&&(this.blendSrc=e.blendSrc),e.blendDst!==void 0&&(this.blendDst=e.blendDst),e.blendEquation!==void 0&&(this.blendEquation=e.blendEquation),e.blendSrcAlpha!==void 0&&(this.blendSrcAlpha=e.blendSrcAlpha),e.blendDstAlpha!==void 0&&(this.blendDstAlpha=e.blendDstAlpha),e.blendEquationAlpha!==void 0&&(this.blendEquationAlpha=e.blendEquationAlpha),e.blendColor!==void 0&&this.blendColor!==void 0&&this.blendColor.setHex(e.blendColor),e.blendAlpha!==void 0&&(this.blendAlpha=e.blendAlpha),e.stencilWriteMask!==void 0&&(this.stencilWriteMask=e.stencilWriteMask),e.stencilFunc!==void 0&&(this.stencilFunc=e.stencilFunc),e.stencilRef!==void 0&&(this.stencilRef=e.stencilRef),e.stencilFuncMask!==void 0&&(this.stencilFuncMask=e.stencilFuncMask),e.stencilFail!==void 0&&(this.stencilFail=e.stencilFail),e.stencilZFail!==void 0&&(this.stencilZFail=e.stencilZFail),e.stencilZPass!==void 0&&(this.stencilZPass=e.stencilZPass),e.stencilWrite!==void 0&&(this.stencilWrite=e.stencilWrite),e.wireframe!==void 0&&(this.wireframe=e.wireframe),e.wireframeLinewidth!==void 0&&(this.wireframeLinewidth=e.wireframeLinewidth),e.wireframeLinecap!==void 0&&(this.wireframeLinecap=e.wireframeLinecap),e.wireframeLinejoin!==void 0&&(this.wireframeLinejoin=e.wireframeLinejoin),e.rotation!==void 0&&(this.rotation=e.rotation),e.linewidth!==void 0&&(this.linewidth=e.linewidth),e.linecap!==void 0&&(this.linecap=e.linecap),e.linejoin!==void 0&&(this.linejoin=e.linejoin),e.dashSize!==void 0&&(this.dashSize=e.dashSize),e.gapSize!==void 0&&(this.gapSize=e.gapSize),e.scale!==void 0&&(this.scale=e.scale),e.polygonOffset!==void 0&&(this.polygonOffset=e.polygonOffset),e.polygonOffsetFactor!==void 0&&(this.polygonOffsetFactor=e.polygonOffsetFactor),e.polygonOffsetUnits!==void 0&&(this.polygonOffsetUnits=e.polygonOffsetUnits),e.dithering!==void 0&&(this.dithering=e.dithering),e.alphaToCoverage!==void 0&&(this.alphaToCoverage=e.alphaToCoverage),e.premultipliedAlpha!==void 0&&(this.premultipliedAlpha=e.premultipliedAlpha),e.forceSinglePass!==void 0&&(this.forceSinglePass=e.forceSinglePass),e.allowOverride!==void 0&&(this.allowOverride=e.allowOverride),e.visible!==void 0&&(this.visible=e.visible),e.toneMapped!==void 0&&(this.toneMapped=e.toneMapped),e.userData!==void 0&&(this.userData=e.userData),e.vertexColors!==void 0&&(typeof e.vertexColors=="number"?this.vertexColors=e.vertexColors>0:this.vertexColors=e.vertexColors),e.size!==void 0&&(this.size=e.size),e.sizeAttenuation!==void 0&&(this.sizeAttenuation=e.sizeAttenuation),e.map!==void 0&&(this.map=t[e.map]||null),e.matcap!==void 0&&(this.matcap=t[e.matcap]||null),e.alphaMap!==void 0&&(this.alphaMap=t[e.alphaMap]||null),e.bumpMap!==void 0&&(this.bumpMap=t[e.bumpMap]||null),e.bumpScale!==void 0&&(this.bumpScale=e.bumpScale),e.normalMap!==void 0&&(this.normalMap=t[e.normalMap]||null),e.normalMapType!==void 0&&(this.normalMapType=e.normalMapType),e.normalScale!==void 0){let i=e.normalScale;Array.isArray(i)===!1&&(i=[i,i]),this.normalScale=new Pe().fromArray(i)}return e.displacementMap!==void 0&&(this.displacementMap=t[e.displacementMap]||null),e.displacementScale!==void 0&&(this.displacementScale=e.displacementScale),e.displacementBias!==void 0&&(this.displacementBias=e.displacementBias),e.roughnessMap!==void 0&&(this.roughnessMap=t[e.roughnessMap]||null),e.metalnessMap!==void 0&&(this.metalnessMap=t[e.metalnessMap]||null),e.emissiveMap!==void 0&&(this.emissiveMap=t[e.emissiveMap]||null),e.emissiveIntensity!==void 0&&(this.emissiveIntensity=e.emissiveIntensity),e.specularMap!==void 0&&(this.specularMap=t[e.specularMap]||null),e.specularIntensityMap!==void 0&&(this.specularIntensityMap=t[e.specularIntensityMap]||null),e.specularColorMap!==void 0&&(this.specularColorMap=t[e.specularColorMap]||null),e.envMap!==void 0&&(this.envMap=t[e.envMap]||null),e.envMapRotation!==void 0&&this.envMapRotation.fromArray(e.envMapRotation),e.envMapIntensity!==void 0&&(this.envMapIntensity=e.envMapIntensity),e.reflectivity!==void 0&&(this.reflectivity=e.reflectivity),e.refractionRatio!==void 0&&(this.refractionRatio=e.refractionRatio),e.lightMap!==void 0&&(this.lightMap=t[e.lightMap]||null),e.lightMapIntensity!==void 0&&(this.lightMapIntensity=e.lightMapIntensity),e.aoMap!==void 0&&(this.aoMap=t[e.aoMap]||null),e.aoMapIntensity!==void 0&&(this.aoMapIntensity=e.aoMapIntensity),e.gradientMap!==void 0&&(this.gradientMap=t[e.gradientMap]||null),e.clearcoatMap!==void 0&&(this.clearcoatMap=t[e.clearcoatMap]||null),e.clearcoatRoughnessMap!==void 0&&(this.clearcoatRoughnessMap=t[e.clearcoatRoughnessMap]||null),e.clearcoatNormalMap!==void 0&&(this.clearcoatNormalMap=t[e.clearcoatNormalMap]||null),e.clearcoatNormalScale!==void 0&&(this.clearcoatNormalScale=new Pe().fromArray(e.clearcoatNormalScale)),e.iridescenceMap!==void 0&&(this.iridescenceMap=t[e.iridescenceMap]||null),e.iridescenceThicknessMap!==void 0&&(this.iridescenceThicknessMap=t[e.iridescenceThicknessMap]||null),e.transmissionMap!==void 0&&(this.transmissionMap=t[e.transmissionMap]||null),e.thicknessMap!==void 0&&(this.thicknessMap=t[e.thicknessMap]||null),e.anisotropyMap!==void 0&&(this.anisotropyMap=t[e.anisotropyMap]||null),e.sheenColorMap!==void 0&&(this.sheenColorMap=t[e.sheenColorMap]||null),e.sheenRoughnessMap!==void 0&&(this.sheenRoughnessMap=t[e.sheenRoughnessMap]||null),this}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;let t=e.clippingPlanes,i=null;if(t!==null){let s=t.length;i=new Array(s);for(let r=0;r!==s;++r)i[r]=t[r].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.allowOverride=e.allowOverride,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}},Li=class extends ni{constructor(e){super(),this.isSpriteMaterial=!0,this.type="SpriteMaterial",this.color=new ke(16777215),this.map=null,this.alphaMap=null,this.rotation=0,this.sizeAttenuation=!0,this.transparent=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.alphaMap=e.alphaMap,this.rotation=e.rotation,this.sizeAttenuation=e.sizeAttenuation,this.fog=e.fog,this}},Do,ka=new y,No=new y,Uo=new y,Fo=new Pe,Va=new Pe,o0=new rt,uc=new y,za=new y,dc=new y,Xp=new Pe,Qu=new Pe,qp=new Pe,es=class extends an{constructor(e=new Li){if(super(),this.isSprite=!0,this.type="Sprite",Do===void 0){Do=new tn;let t=new Float32Array([-.5,-.5,0,0,0,.5,-.5,0,1,0,.5,.5,0,1,1,-.5,.5,0,0,1]),i=new Xr(t,5);Do.setIndex([0,1,2,0,2,3]),Do.setAttribute("position",new cr(i,3,0,!1)),Do.setAttribute("uv",new cr(i,2,3,!1))}this.geometry=Do,this.material=e,this.center=new Pe(.5,.5),this.count=1}intersectsFrustum(e){return e.intersectsSprite(this)}raycast(e,t){e.camera===null&&ht('Sprite: "Raycaster.camera" needs to be set in order to raycast against sprites.'),No.setFromMatrixScale(this.matrixWorld),o0.copy(e.camera.matrixWorld),this.modelViewMatrix.multiplyMatrices(e.camera.matrixWorldInverse,this.matrixWorld),Uo.setFromMatrixPosition(this.modelViewMatrix),e.camera.isPerspectiveCamera&&this.material.sizeAttenuation===!1&&No.multiplyScalar(-Uo.z);let i=this.material.rotation,s,r;i!==0&&(r=Math.cos(i),s=Math.sin(i));let o=this.center;fc(uc.set(-.5,-.5,0),Uo,o,No,s,r),fc(za.set(.5,-.5,0),Uo,o,No,s,r),fc(dc.set(.5,.5,0),Uo,o,No,s,r),Xp.set(0,0),Qu.set(1,0),qp.set(1,1);let a=e.ray.intersectTriangle(uc,za,dc,!1,ka);if(a===null&&(fc(za.set(-.5,.5,0),Uo,o,No,s,r),Qu.set(0,1),a=e.ray.intersectTriangle(uc,dc,za,!1,ka),a===null))return;let c=e.ray.origin.distanceTo(ka);c<e.near||c>e.far||t.push({distance:c,point:ka.clone(),uv:gs.getInterpolation(ka,uc,za,dc,Xp,Qu,qp,new Pe),face:null,object:this})}copy(e,t){return super.copy(e,t),e.center!==void 0&&this.center.copy(e.center),this.material=e.material,this}};function fc(n,e,t,i,s,r){Fo.subVectors(n,t).addScalar(.5).multiply(i),s!==void 0?(Va.x=r*Fo.x-s*Fo.y,Va.y=s*Fo.x+r*Fo.y):Va.copy(Fo),n.copy(e),n.x+=Va.x,n.y+=Va.y,n.applyMatrix4(o0)}var Bs=new y,ed=new y,pc=new y,mc=new y,vs=class{constructor(e=new y,t=new y(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,Bs)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);let i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){let t=Bs.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(Bs.copy(this.origin).addScaledVector(this.direction,t),Bs.distanceToSquared(e))}distanceSqToSegment(e,t,i,s){ed.copy(e).add(t).multiplyScalar(.5),pc.copy(t).sub(e).normalize(),mc.copy(this.origin).sub(ed);let r=e.distanceTo(t)*.5,o=-this.direction.dot(pc),a=mc.dot(this.direction),c=-mc.dot(pc),l=mc.lengthSq(),u=Math.abs(1-o*o),d,f,p,x;if(u>0)if(d=o*c-a,f=o*a-c,x=r*u,d>=0)if(f>=-x)if(f<=x){let b=1/u;d*=b,f*=b,p=d*(d+o*f+2*a)+f*(o*d+f+2*c)+l}else f=r,d=Math.max(0,-(o*f+a)),p=-d*d+f*(f+2*c)+l;else f=-r,d=Math.max(0,-(o*f+a)),p=-d*d+f*(f+2*c)+l;else f<=-x?(d=Math.max(0,-(-o*r+a)),f=d>0?-r:Math.min(Math.max(-r,-c),r),p=-d*d+f*(f+2*c)+l):f<=x?(d=0,f=Math.min(Math.max(-r,-c),r),p=f*(f+2*c)+l):(d=Math.max(0,-(o*r+a)),f=d>0?r:Math.min(Math.max(-r,-c),r),p=-d*d+f*(f+2*c)+l);else f=o>0?-r:r,d=Math.max(0,-(o*f+a)),p=-d*d+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,d),s&&s.copy(ed).addScaledVector(pc,f),p}intersectSphere(e,t){if(e.radius<0)return null;Bs.subVectors(e.center,this.origin);let i=Bs.dot(this.direction),s=Bs.dot(Bs)-i*i,r=e.radius*e.radius;if(s>r)return null;let o=Math.sqrt(r-s),a=i-o,c=i+o;return c<0?null:a<0?this.at(c,t):this.at(a,t)}intersectsSphere(e){return e.radius<0?!1:this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){let t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;let i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){let i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){let t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,s,r,o,a,c,l=1/this.direction.x,u=1/this.direction.y,d=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,s=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,s=(e.min.x-f.x)*l),u>=0?(r=(e.min.y-f.y)*u,o=(e.max.y-f.y)*u):(r=(e.max.y-f.y)*u,o=(e.min.y-f.y)*u),i>o||r>s||((r>i||isNaN(i))&&(i=r),(o<s||isNaN(s))&&(s=o),d>=0?(a=(e.min.z-f.z)*d,c=(e.max.z-f.z)*d):(a=(e.max.z-f.z)*d,c=(e.min.z-f.z)*d),i>c||a>s)||((a>i||i!==i)&&(i=a),(c<s||s!==s)&&(s=c),s<0)?null:this.at(i>=0?i:s,t)}intersectsBox(e){return this.intersectBox(e,Bs)!==null}intersectTriangle(e,t,i,s,r){let o=this.origin,a=this.direction,c=a.x,l=a.y,u=a.z,d=e.x-o.x,f=e.y-o.y,p=e.z-o.z,x=t.x-o.x,b=t.y-o.y,g=t.z-o.z,m=i.x-o.x,A=i.y-o.y,U=i.z-o.z,T=Math.abs(c),I=Math.abs(l),L=Math.abs(u),P,M,C,O,H,k,q,z,ee,he,ue,ye;if(T>=I&&T>=L?(C=c,k=d,ee=x,ye=m,c>=0?(P=l,M=u,O=f,H=p,q=b,z=g,he=A,ue=U):(P=u,M=l,O=p,H=f,q=g,z=b,he=U,ue=A)):I>=L?(C=l,k=f,ee=b,ye=A,l>=0?(P=u,M=c,O=p,H=d,q=g,z=x,he=U,ue=m):(P=c,M=u,O=d,H=p,q=x,z=g,he=m,ue=U)):(C=u,k=p,ee=g,ye=U,u>=0?(P=c,M=l,O=d,H=f,q=x,z=b,he=m,ue=A):(P=l,M=c,O=f,H=d,q=b,z=x,he=A,ue=m)),C===0)return null;let V=P/C,Q=M/C,le=1/C,Ee=O-V*k,be=H-Q*k,ut=q-V*ee,et=z-Q*ee,ct=he-V*ye,ae=ue-Q*ye,me=ct*et-ae*ut,qe=Ee*ae-be*ct,ft=ut*be-et*Ee;if(s){if(me<0||qe<0||ft<0)return null}else if((me<0||qe<0||ft<0)&&(me>0||qe>0||ft>0))return null;let Ge=me+qe+ft;if(Ge===0)return null;let Et=le*(me*k+qe*ee+ft*ye);return(Ge>0?Et<0:Et>0)?null:this.at(Et/Ge,r)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},ln=class extends ni{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ke(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Pi,this.combine=Id,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}},Yp=new rt,Br=new vs,gc=new li,$p=new y,_c=new y,xc=new y,vc=new y,td=new y,yc=new y,Zp=new y,Mc=new y,dn=class extends an{constructor(e=new tn,t=new ln){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let s=t[i[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,o=s.length;r<o;r++){let a=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[a]=r}}}}getVertexPosition(e,t){let i=this.geometry,s=i.attributes.position,r=i.morphAttributes.position,o=i.morphTargetsRelative;t.fromBufferAttribute(s,e);let a=this.morphTargetInfluences;if(r&&a){yc.set(0,0,0);for(let c=0,l=r.length;c<l;c++){let u=a[c],d=r[c];u!==0&&(td.fromBufferAttribute(d,e),o?yc.addScaledVector(td,u):yc.addScaledVector(td.sub(t),u))}t.add(yc)}return t}intersectsFrustum(e){return e.intersectsObject(this)}raycast(e,t){let i=this.geometry,s=this.material,r=this.matrixWorld;s!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),gc.copy(i.boundingSphere),gc.applyMatrix4(r),Br.copy(e.ray).recast(e.near),!(gc.containsPoint(Br.origin)===!1&&(Br.intersectSphere(gc,$p)===null||Br.origin.distanceToSquared($p)>(e.far-e.near)**2))&&(Yp.copy(r).invert(),Br.copy(e.ray).applyMatrix4(Yp),!(i.boundingBox!==null&&Br.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,Br)))}_computeIntersections(e,t,i){let s,r=this.geometry,o=this.material,a=r.index,c=r.attributes.position,l=r.attributes.uv,u=r.attributes.uv1,d=r.attributes.normal,f=r.groups,p=r.drawRange;if(a!==null)if(Array.isArray(o))for(let x=0,b=f.length;x<b;x++){let g=f[x],m=o[g.materialIndex],A=Math.max(g.start,p.start),U=Math.min(a.count,Math.min(g.start+g.count,p.start+p.count));for(let T=A,I=U;T<I;T+=3){let L=a.getX(T),P=a.getX(T+1),M=a.getX(T+2);s=Ec(this,m,e,i,l,u,d,L,P,M),s&&(s.faceIndex=Math.floor(T/3),s.face.materialIndex=g.materialIndex,t.push(s))}}else{let x=Math.max(0,p.start),b=Math.min(a.count,p.start+p.count);for(let g=x,m=b;g<m;g+=3){let A=a.getX(g),U=a.getX(g+1),T=a.getX(g+2);s=Ec(this,o,e,i,l,u,d,A,U,T),s&&(s.faceIndex=Math.floor(g/3),t.push(s))}}else if(c!==void 0)if(Array.isArray(o))for(let x=0,b=f.length;x<b;x++){let g=f[x],m=o[g.materialIndex],A=Math.max(g.start,p.start),U=Math.min(c.count,Math.min(g.start+g.count,p.start+p.count));for(let T=A,I=U;T<I;T+=3){let L=T,P=T+1,M=T+2;s=Ec(this,m,e,i,l,u,d,L,P,M),s&&(s.faceIndex=Math.floor(T/3),s.face.materialIndex=g.materialIndex,t.push(s))}}else{let x=Math.max(0,p.start),b=Math.min(c.count,p.start+p.count);for(let g=x,m=b;g<m;g+=3){let A=g,U=g+1,T=g+2;s=Ec(this,o,e,i,l,u,d,A,U,T),s&&(s.faceIndex=Math.floor(g/3),t.push(s))}}}};function P_(n,e,t,i,s,r,o,a){let c;if(e.side===Hn?c=i.intersectTriangle(o,r,s,!0,a):c=i.intersectTriangle(s,r,o,e.side===Es,a),c===null)return null;Mc.copy(a),Mc.applyMatrix4(n.matrixWorld);let l=t.ray.origin.distanceTo(Mc);return l<t.near||l>t.far?null:{distance:l,point:Mc.clone(),object:n}}function Ec(n,e,t,i,s,r,o,a,c,l){n.getVertexPosition(a,_c),n.getVertexPosition(c,xc),n.getVertexPosition(l,vc);let u=P_(n,e,t,i,_c,xc,vc,Zp);if(u){let d=new y;gs.getBarycoord(Zp,_c,xc,vc,d),s&&(u.uv=gs.getInterpolatedAttribute(s,a,c,l,d,new Pe)),r&&(u.uv1=gs.getInterpolatedAttribute(r,a,c,l,d,new Pe)),o&&(u.normal=gs.getInterpolatedAttribute(o,a,c,l,d,new y),u.normal.dot(i.direction)>0&&u.normal.multiplyScalar(-1));let f={a,b:c,c:l,normal:new y,materialIndex:0};gs.getNormal(_c,xc,vc,f.normal),u.face=f,u.barycoord=d}return u}var Ga=new $t,Kp=new $t,jp=new $t,L_=new $t,Jp=new rt,bc=new y,nd=new li,Qp=new rt,id=new vs,tl=class extends dn{constructor(e,t){super(e,t),this.isSkinnedMesh=!0,this.type="SkinnedMesh",this.bindMode=ud,this.bindMatrix=new rt,this.bindMatrixInverse=new rt,this.boundingBox=null,this.boundingSphere=null}computeBoundingBox(){let e=this.geometry;this.boundingBox===null&&(this.boundingBox=new un),this.boundingBox.makeEmpty();let t=e.getAttribute("position");for(let i=0;i<t.count;i++)this.getVertexPosition(i,bc),this.boundingBox.expandByPoint(bc)}computeBoundingSphere(){let e=this.geometry;this.boundingSphere===null&&(this.boundingSphere=new li),this.boundingSphere.makeEmpty();let t=e.getAttribute("position");for(let i=0;i<t.count;i++)this.getVertexPosition(i,bc),this.boundingSphere.expandByPoint(bc)}copy(e,t){return super.copy(e,t),this.bindMode=e.bindMode,this.bindMatrix.copy(e.bindMatrix),this.bindMatrixInverse.copy(e.bindMatrixInverse),this.skeleton=e.skeleton,e.boundingBox!==null&&(this.boundingBox=e.boundingBox.clone()),e.boundingSphere!==null&&(this.boundingSphere=e.boundingSphere.clone()),this}raycast(e,t){let i=this.material,s=this.matrixWorld;i!==void 0&&(this.boundingSphere===null&&this.computeBoundingSphere(),nd.copy(this.boundingSphere),nd.applyMatrix4(s),e.ray.intersectsSphere(nd)!==!1&&(Qp.copy(s).invert(),id.copy(e.ray).applyMatrix4(Qp),!(this.boundingBox!==null&&id.intersectsBox(this.boundingBox)===!1)&&this._computeIntersections(e,t,id)))}getVertexPosition(e,t){return super.getVertexPosition(e,t),this.applyBoneTransform(e,t),t}bind(e,t){this.skeleton=e,t===void 0&&(this.updateMatrixWorld(!0),this.skeleton.calculateInverses(),t=this.matrixWorld),this.bindMatrix.copy(t),this.bindMatrixInverse.copy(t).invert()}pose(){this.skeleton.pose()}normalizeSkinWeights(){let e=new $t,t=this.geometry.attributes.skinWeight;for(let i=0,s=t.count;i<s;i++){e.fromBufferAttribute(t,i);let r=1/e.manhattanLength();r!==1/0?e.multiplyScalar(r):e.set(1,0,0,0),t.setXYZW(i,e.x,e.y,e.z,e.w)}}updateMatrixWorld(e){super.updateMatrixWorld(e),this.bindMode===ud?this.bindMatrixInverse.copy(this.matrixWorld).invert():this.bindMode===Wm?this.bindMatrixInverse.copy(this.bindMatrix).invert():nt("SkinnedMesh: Unrecognized bindMode: "+this.bindMode)}applyBoneTransform(e,t){let i=this.skeleton,s=this.geometry;Kp.fromBufferAttribute(s.attributes.skinIndex,e),jp.fromBufferAttribute(s.attributes.skinWeight,e),t.isVector4?(Ga.copy(t),t.set(0,0,0,0)):(Ga.set(...t,1),t.set(0,0,0)),Ga.applyMatrix4(this.bindMatrix);for(let r=0;r<4;r++){let o=jp.getComponent(r);if(o!==0){let a=Kp.getComponent(r);Jp.multiplyMatrices(i.bones[a].matrixWorld,i.boneInverses[a]),t.addScaledVector(L_.copy(Ga).applyMatrix4(Jp),o)}}return t.isVector4&&(t.w=Ga.w),t.applyMatrix4(this.bindMatrixInverse)}},Jo=class extends an{constructor(){super(),this.isBone=!0,this.type="Bone"}},Qo=class extends In{constructor(e=null,t=1,i=1,s,r,o,a,c,l=vn,u=vn,d,f){super(null,o,a,c,l,u,s,r,d,f),this.isDataTexture=!0,this.image={data:e,width:t,height:i},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}},em=new rt,D_=new rt,nl=class n{constructor(e=[],t=[]){this.uuid=Ji(),this.bones=e.slice(0),this.boneInverses=t,this.boneMatrices=null,this.boneTexture=null,this.init()}init(){let e=this.bones,t=this.boneInverses;if(this.boneMatrices=new Float32Array(e.length*16),t.length===0)this.calculateInverses();else if(e.length!==t.length){nt("Skeleton: Number of inverse bone matrices does not match amount of bones."),this.boneInverses=[];for(let i=0,s=this.bones.length;i<s;i++)this.boneInverses.push(new rt)}}calculateInverses(){this.boneInverses.length=0;for(let e=0,t=this.bones.length;e<t;e++){let i=new rt;this.bones[e]&&i.copy(this.bones[e].matrixWorld).invert(),this.boneInverses.push(i)}}pose(){for(let e=0,t=this.bones.length;e<t;e++){let i=this.bones[e];i&&i.matrixWorld.copy(this.boneInverses[e]).invert()}for(let e=0,t=this.bones.length;e<t;e++){let i=this.bones[e];i&&(i.parent&&i.parent.isBone?(i.matrix.copy(i.parent.matrixWorld).invert(),i.matrix.multiply(i.matrixWorld)):i.matrix.copy(i.matrixWorld),i.matrix.decompose(i.position,i.quaternion,i.scale))}}update(){let e=this.bones,t=this.boneInverses,i=this.boneMatrices,s=this.boneTexture;for(let r=0,o=e.length;r<o;r++){let a=e[r]?e[r].matrixWorld:D_;em.multiplyMatrices(a,t[r]),em.toArray(i,r*16)}s!==null&&(s.needsUpdate=!0)}clone(){return new n(this.bones,this.boneInverses)}computeBoneTexture(){let e=Math.sqrt(this.bones.length*4);e=Math.ceil(e/4)*4,e=Math.max(e,4);let t=new Float32Array(e*e*4);t.set(this.boneMatrices);let i=new Qo(t,e,e,Si,Ti);return i.needsUpdate=!0,this.boneMatrices=t,this.boneTexture=i,this}getBoneByName(e){for(let t=0,i=this.bones.length;t<i;t++){let s=this.bones[t];if(s.name===e)return s}}dispose(){this.boneTexture!==null&&(this.boneTexture.dispose(),this.boneTexture=null)}fromJSON(e,t){this.uuid=e.uuid;for(let i=0,s=e.bones.length;i<s;i++){let r=e.bones[i],o=t[r];o===void 0&&(nt("Skeleton: No bone found with UUID:",r),o=new Jo),this.bones.push(o),this.boneInverses.push(new rt().fromArray(e.boneInverses[i]))}return this.init(),this}toJSON(){let e={metadata:{version:4.7,type:"Skeleton",generator:"Skeleton.toJSON"},bones:[],boneInverses:[]};e.uuid=this.uuid;let t=this.bones,i=this.boneInverses;for(let s=0,r=t.length;s<r;s++){let o=t[s];e.bones.push(o.uuid);let a=i[s];e.boneInverses.push(a.toArray())}return e}},Vs=class extends Cn{constructor(e,t,i,s=1){super(e,t,i),this.isInstancedBufferAttribute=!0,this.meshPerAttribute=s}copy(e){return super.copy(e),this.meshPerAttribute=e.meshPerAttribute,this}toJSON(){let e=super.toJSON();return e.meshPerAttribute=this.meshPerAttribute,e.isInstancedBufferAttribute=!0,e}},Oo=new rt,tm=new rt,Tc=[],nm=new un,N_=new rt,Wa=new dn,Xa=new li,ii=class extends dn{constructor(e,t,i){super(e,t),this.isInstancedMesh=!0,this.instanceMatrix=new Vs(new Float32Array(i*16),16),this.instanceColor=null,this.morphTexture=null,this.count=i,this.boundingBox=null,this.boundingSphere=null;for(let s=0;s<i;s++)this.setMatrixAt(s,N_)}computeBoundingBox(){let e=this.geometry,t=this.count;this.boundingBox===null&&(this.boundingBox=new un),e.boundingBox===null&&e.computeBoundingBox(),this.boundingBox.makeEmpty();for(let i=0;i<t;i++)this.getMatrixAt(i,Oo),nm.copy(e.boundingBox).applyMatrix4(Oo),this.boundingBox.union(nm)}computeBoundingSphere(){let e=this.geometry,t=this.count;this.boundingSphere===null&&(this.boundingSphere=new li),e.boundingSphere===null&&e.computeBoundingSphere(),this.boundingSphere.makeEmpty();for(let i=0;i<t;i++)this.getMatrixAt(i,Oo),Xa.copy(e.boundingSphere).applyMatrix4(Oo),this.boundingSphere.union(Xa)}copy(e,t){return super.copy(e,t),this.instanceMatrix.copy(e.instanceMatrix),e.morphTexture!==null&&(this.morphTexture=e.morphTexture.clone()),e.instanceColor!==null&&(this.instanceColor=e.instanceColor.clone()),this.count=e.count,e.boundingBox!==null&&(this.boundingBox=e.boundingBox.clone()),e.boundingSphere!==null&&(this.boundingSphere=e.boundingSphere.clone()),this}getColorAt(e,t){return this.instanceColor===null?t.setRGB(1,1,1):t.fromArray(this.instanceColor.array,e*3)}getMatrixAt(e,t){return t.fromArray(this.instanceMatrix.array,e*16)}getMorphAt(e,t){let i=t.morphTargetInfluences,s=this.morphTexture.source.data.data,r=i.length+1,o=e*r+1;for(let a=0;a<i.length;a++)i[a]=s[o+a]}raycast(e,t){let i=this.matrixWorld,s=this.count;if(Wa.geometry=this.geometry,Wa.material=this.material,Wa.material!==void 0&&(this.boundingSphere===null&&this.computeBoundingSphere(),Xa.copy(this.boundingSphere),Xa.applyMatrix4(i),e.ray.intersectsSphere(Xa)!==!1))for(let r=0;r<s;r++){this.getMatrixAt(r,Oo),tm.multiplyMatrices(i,Oo),Wa.matrixWorld=tm,Wa.raycast(e,Tc);for(let o=0,a=Tc.length;o<a;o++){let c=Tc[o];c.instanceId=r,c.object=this,t.push(c)}Tc.length=0}}setColorAt(e,t){return this.instanceColor===null&&(this.instanceColor=new Vs(new Float32Array(this.instanceMatrix.count*3).fill(1),3)),t.toArray(this.instanceColor.array,e*3),this}setMatrixAt(e,t){return t.toArray(this.instanceMatrix.array,e*16),this}setMorphAt(e,t){let i=t.morphTargetInfluences,s=i.length+1;this.morphTexture===null&&(this.morphTexture=new Qo(new Float32Array(s*this.count),s,this.count,bh,Ti));let r=this.morphTexture.source.data.data,o=0;for(let l=0;l<i.length;l++)o+=i[l];let a=this.geometry.morphTargetsRelative?1:1-o,c=s*e;return r[c]=a,r.set(i,c+1),this}updateMorphTargets(){}dispose(){super.dispose(),this.morphTexture!==null&&(this.morphTexture.dispose(),this.morphTexture=null)}},Hr=new li,U_=new Pe(.5,.5),Sc=new y,ea=class{constructor(e=new Bn,t=new Bn,i=new Bn,s=new Bn,r=new Bn,o=new Bn){this.planes=[e,t,i,s,r,o]}set(e,t,i,s,r,o){let a=this.planes;return a[0].copy(e),a[1].copy(t),a[2].copy(i),a[3].copy(s),a[4].copy(r),a[5].copy(o),this}copy(e){let t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=ji,i=!1){let s=this.planes,r=e.elements,o=r[0],a=r[1],c=r[2],l=r[3],u=r[4],d=r[5],f=r[6],p=r[7],x=r[8],b=r[9],g=r[10],m=r[11],A=r[12],U=r[13],T=r[14],I=r[15];if(s[0].setComponents(l-o,p-u,m-x,I-A).normalize(),s[1].setComponents(l+o,p+u,m+x,I+A).normalize(),s[2].setComponents(l+a,p+d,m+b,I+U).normalize(),s[3].setComponents(l-a,p-d,m-b,I-U).normalize(),i)s[4].setComponents(c,f,g,T).normalize(),s[5].setComponents(l-c,p-f,m-g,I-T).normalize();else if(s[4].setComponents(l-c,p-f,m-g,I-T).normalize(),t===ji)s[5].setComponents(l+c,p+f,m+g,I+T).normalize();else if(t===Xo)s[5].setComponents(c,f,g,T).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),Hr.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{let t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),Hr.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(Hr)}intersectsSprite(e){Hr.center.set(0,0,0);let t=U_.distanceTo(e.center);return Hr.radius=.7071067811865476+t,Hr.applyMatrix4(e.matrixWorld),this.intersectsSphere(Hr)}intersectsSphere(e){let t=this.planes,i=e.center,s=-e.radius;for(let r=0;r<6;r++)if(t[r].distanceToPoint(i)<s)return!1;return!0}intersectsBox(e){let t=this.planes;for(let i=0;i<6;i++){let s=t[i];if(Sc.x=s.normal.x>0?e.max.x:e.min.x,Sc.y=s.normal.y>0?e.max.y:e.min.y,Sc.z=s.normal.z>0?e.max.z:e.min.z,s.distanceToPoint(Sc)<0)return!1}return!0}containsPoint(e){let t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}};var zs=class extends ni{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ke(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}},$c=new y,Zc=new y,im=new rt,qa=new vs,wc=new li,sd=new y,sm=new y,qr=class extends an{constructor(e=new tn,t=new zs){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,i=[0];for(let s=1,r=t.count;s<r;s++)$c.fromBufferAttribute(t,s-1),Zc.fromBufferAttribute(t,s),i[s]=i[s-1],i[s]+=$c.distanceTo(Zc);e.setAttribute("lineDistance",new Dt(i,1))}else nt("Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}intersectsFrustum(e){return e.intersectsObject(this)}raycast(e,t){let i=this.geometry,s=this.matrixWorld,r=e.params.Line.threshold,o=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),wc.copy(i.boundingSphere),wc.applyMatrix4(s),wc.radius+=r,e.ray.intersectsSphere(wc)===!1)return;im.copy(s).invert(),qa.copy(e.ray).applyMatrix4(im);let a=r/((this.scale.x+this.scale.y+this.scale.z)/3),c=a*a,l=this.isLineSegments?2:1,u=i.index,f=i.attributes.position;if(u!==null){let p=Math.max(0,o.start),x=Math.min(u.count,o.start+o.count);for(let b=p,g=x-1;b<g;b+=l){let m=u.getX(b),A=u.getX(b+1),U=Ac(this,e,qa,c,m,A,b);U&&t.push(U)}if(this.isLineLoop){let b=u.getX(x-1),g=u.getX(p),m=Ac(this,e,qa,c,b,g,x-1);m&&t.push(m)}}else{let p=Math.max(0,o.start),x=Math.min(f.count,o.start+o.count);for(let b=p,g=x-1;b<g;b+=l){let m=Ac(this,e,qa,c,b,b+1,b);m&&t.push(m)}if(this.isLineLoop){let b=Ac(this,e,qa,c,x-1,p,x-1);b&&t.push(b)}}}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let s=t[i[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,o=s.length;r<o;r++){let a=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[a]=r}}}}};function Ac(n,e,t,i,s,r,o){let a=n.geometry.attributes.position;if($c.fromBufferAttribute(a,s),Zc.fromBufferAttribute(a,r),t.distanceSqToSegment($c,Zc,sd,sm)>i)return;sd.applyMatrix4(n.matrixWorld);let l=e.ray.origin.distanceTo(sd);if(!(l<e.near||l>e.far))return{distance:l,point:sm.clone().applyMatrix4(n.matrixWorld),index:o,face:null,faceIndex:null,barycoord:null,object:n}}var rm=new y,om=new y,hr=class extends qr{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,i=[];for(let s=0,r=t.count;s<r;s+=2)rm.fromBufferAttribute(t,s),om.fromBufferAttribute(t,s+1),i[s]=s===0?0:i[s-1],i[s+1]=i[s]+rm.distanceTo(om);e.setAttribute("lineDistance",new Dt(i,1))}else nt("LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}},il=class extends qr{constructor(e,t){super(e,t),this.isLineLoop=!0,this.type="LineLoop"}},ur=class extends ni{constructor(e){super(),this.isPointsMaterial=!0,this.type="PointsMaterial",this.color=new ke(16777215),this.map=null,this.alphaMap=null,this.size=1,this.sizeAttenuation=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.alphaMap=e.alphaMap,this.size=e.size,this.sizeAttenuation=e.sizeAttenuation,this.fog=e.fog,this}},am=new rt,gd=new vs,Rc=new li,Cc=new y,Yr=class extends an{constructor(e=new tn,t=new ur){super(),this.isPoints=!0,this.type="Points",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}intersectsFrustum(e){return e.intersectsObject(this)}raycast(e,t){let i=this.geometry,s=this.matrixWorld,r=e.params.Points.threshold,o=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),Rc.copy(i.boundingSphere),Rc.applyMatrix4(s),Rc.radius+=r,e.ray.intersectsSphere(Rc)===!1)return;am.copy(s).invert(),gd.copy(e.ray).applyMatrix4(am);let a=r/((this.scale.x+this.scale.y+this.scale.z)/3),c=a*a,l=i.index,d=i.attributes.position;if(l!==null){let f=Math.max(0,o.start),p=Math.min(l.count,o.start+o.count);for(let x=f,b=p;x<b;x++){let g=l.getX(x);Cc.fromBufferAttribute(d,g),lm(Cc,g,c,s,e,t,this)}}else{let f=Math.max(0,o.start),p=Math.min(d.count,o.start+o.count);for(let x=f,b=p;x<b;x++)Cc.fromBufferAttribute(d,x),lm(Cc,x,c,s,e,t,this)}}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let s=t[i[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,o=s.length;r<o;r++){let a=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[a]=r}}}}};function lm(n,e,t,i,s,r,o){let a=gd.distanceSqToPoint(n);if(a<t){let c=new y;gd.closestPointToPoint(n,c),c.applyMatrix4(i);let l=s.ray.origin.distanceTo(c);if(l<s.near||l>s.far)return;r.push({distance:l,distanceToRay:Math.sqrt(a),point:c,index:e,face:null,faceIndex:null,barycoord:null,object:o})}}var sl=class extends In{constructor(e=[],t=gr,i,s,r,o,a,c,l,u){super(e,t,i,s,r,o,a,c,l,u),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}},ci=class extends In{constructor(e,t,i,s,r,o,a,c,l){super(e,t,i,s,r,o,a,c,l),this.isCanvasTexture=!0,this.needsUpdate=!0}};var dr=class extends In{constructor(e,t,i=ss,s,r,o,a=vn,c=vn,l,u=xs,d=1){if(u!==xs&&u!==_r)throw new Error("THREE.DepthTexture: format must be either THREE.DepthFormat or THREE.DepthStencilFormat");let f={width:e,height:t,depth:d};super(f,s,r,o,a,c,u,i,l),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new $o(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){let t=super.toJSON(e);return t.compareFunction=this.compareFunction,t}},Kc=class extends dr{constructor(e,t=ss,i=gr,s,r,o=vn,a=vn,c,l=xs){let u={width:e,height:e,depth:1},d=[u,u,u,u,u,u];super(e,e,t,i,s,r,o,a,c,l),this.image=d,this.isCubeDepthTexture=!0,this.isCubeTexture=!0}get images(){return this.image}set images(e){this.image=e}},rl=class extends In{constructor(e=null){super(),this.sourceTexture=e,this.isExternalTexture=!0}copy(e){return super.copy(e),this.sourceTexture=e.sourceTexture,this}},_t=class n extends tn{constructor(e=1,t=1,i=1,s=1,r=1,o=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:s,heightSegments:r,depthSegments:o};let a=this;s=Math.floor(s),r=Math.floor(r),o=Math.floor(o);let c=[],l=[],u=[],d=[],f=0,p=0;x("z","y","x",-1,-1,i,t,e,o,r,0),x("z","y","x",1,-1,i,t,-e,o,r,1),x("x","z","y",1,1,e,i,t,s,o,2),x("x","z","y",1,-1,e,i,-t,s,o,3),x("x","y","z",1,-1,e,t,i,s,r,4),x("x","y","z",-1,-1,e,t,-i,s,r,5),this.setIndex(c),this.setAttribute("position",new Dt(l,3)),this.setAttribute("normal",new Dt(u,3)),this.setAttribute("uv",new Dt(d,2));function x(b,g,m,A,U,T,I,L,P,M,C){let O=T/P,H=I/M,k=T/2,q=I/2,z=L/2,ee=P+1,he=M+1,ue=0,ye=0,V=new y;for(let Q=0;Q<he;Q++){let le=Q*H-q;for(let Ee=0;Ee<ee;Ee++){let be=Ee*O-k;V[b]=be*A,V[g]=le*U,V[m]=z,l.push(V.x,V.y,V.z),V[b]=0,V[g]=0,V[m]=L>0?1:-1,u.push(V.x,V.y,V.z),d.push(Ee/P),d.push(1-Q/M),ue+=1}}for(let Q=0;Q<M;Q++)for(let le=0;le<P;le++){let Ee=f+le+ee*Q,be=f+le+ee*(Q+1),ut=f+(le+1)+ee*(Q+1),et=f+(le+1)+ee*Q;c.push(Ee,be,et),c.push(be,ut,et),ye+=6}a.addGroup(p,ye,C),p+=ye,f+=ue}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}};var $r=class n extends tn{constructor(e=1,t=32,i=0,s=Math.PI*2){super(),this.type="CircleGeometry",this.parameters={radius:e,segments:t,thetaStart:i,thetaLength:s},t=Math.max(3,t);let r=[],o=[],a=[],c=[],l=new y,u=new Pe;o.push(0,0,0),a.push(0,0,1),c.push(.5,.5);for(let d=0,f=3;d<=t;d++,f+=3){let p=i+d/t*s;l.x=e*Math.cos(p),l.y=e*Math.sin(p),o.push(l.x,l.y,l.z),a.push(0,0,1),u.x=(o[f]/e+1)/2,u.y=(o[f+1]/e+1)/2,c.push(u.x,u.y)}for(let d=1;d<=t;d++)r.push(d,d+1,0);this.setIndex(r),this.setAttribute("position",new Dt(o,3)),this.setAttribute("normal",new Dt(a,3)),this.setAttribute("uv",new Dt(c,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radius,e.segments,e.thetaStart,e.thetaLength)}},fr=class n extends tn{constructor(e=1,t=1,i=1,s=32,r=1,o=!1,a=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:s,heightSegments:r,openEnded:o,thetaStart:a,thetaLength:c};let l=this;s=Math.floor(s),r=Math.floor(r);let u=[],d=[],f=[],p=[],x=0,b=[],g=i/2,m=0;A(),o===!1&&(e>0&&U(!0),t>0&&U(!1)),this.setIndex(u),this.setAttribute("position",new Dt(d,3)),this.setAttribute("normal",new Dt(f,3)),this.setAttribute("uv",new Dt(p,2));function A(){let T=new y,I=new y,L=0,P=(t-e)/i;for(let M=0;M<=r;M++){let C=[],O=M/r,H=O*(t-e)+e;for(let k=0;k<=s;k++){let q=k/s,z=q*c+a,ee=Math.sin(z),he=Math.cos(z);I.x=H*ee,I.y=-O*i+g,I.z=H*he,d.push(I.x,I.y,I.z),T.set(ee,P,he).normalize(),f.push(T.x,T.y,T.z),p.push(q,1-O),C.push(x++)}b.push(C)}for(let M=0;M<s;M++)for(let C=0;C<r;C++){let O=b[C][M],H=b[C+1][M],k=b[C+1][M+1],q=b[C][M+1];(e>0||C!==0)&&(u.push(O,H,q),L+=3),(t>0||C!==r-1)&&(u.push(H,k,q),L+=3)}l.addGroup(m,L,0),m+=L}function U(T){let I=x,L=new Pe,P=new y,M=0,C=T===!0?e:t,O=T===!0?1:-1;for(let k=1;k<=s;k++)d.push(0,g*O,0),f.push(0,O,0),p.push(.5,.5),x++;let H=x;for(let k=0;k<=s;k++){let z=k/s*c+a,ee=Math.cos(z),he=Math.sin(z);P.x=C*he,P.y=g*O,P.z=C*ee,d.push(P.x,P.y,P.z),f.push(0,O,0),L.x=ee*.5+.5,L.y=he*.5*O+.5,p.push(L.x,L.y),x++}for(let k=0;k<s;k++){let q=I+k,z=H+k;T===!0?u.push(z,z+1,q):u.push(z+1,z,q),M+=3}l.addGroup(m,M,T===!0?1:2),m+=M}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}};var jc=class n extends tn{constructor(e=[],t=[],i=1,s=0){super(),this.type="PolyhedronGeometry",this.parameters={vertices:e,indices:t,radius:i,detail:s};let r=[],o=[];a(s),l(i),u(),this.setAttribute("position",new Dt(r,3)),this.setAttribute("normal",new Dt(r.slice(),3)),this.setAttribute("uv",new Dt(o,2)),s===0?this.computeVertexNormals():this.normalizeNormals();function a(A){let U=new y,T=new y,I=new y;for(let L=0;L<t.length;L+=3)p(t[L+0],U),p(t[L+1],T),p(t[L+2],I),c(U,T,I,A)}function c(A,U,T,I){let L=I+1,P=[];for(let M=0;M<=L;M++){P[M]=[];let C=A.clone().lerp(T,M/L),O=U.clone().lerp(T,M/L),H=L-M;for(let k=0;k<=H;k++)k===0&&M===L?P[M][k]=C:P[M][k]=C.clone().lerp(O,k/H)}for(let M=0;M<L;M++)for(let C=0;C<2*(L-M)-1;C++){let O=Math.floor(C/2);C%2===0?(f(P[M][O+1]),f(P[M+1][O]),f(P[M][O])):(f(P[M][O+1]),f(P[M+1][O+1]),f(P[M+1][O]))}}function l(A){let U=new y;for(let T=0;T<r.length;T+=3)U.x=r[T+0],U.y=r[T+1],U.z=r[T+2],U.normalize().multiplyScalar(A),r[T+0]=U.x,r[T+1]=U.y,r[T+2]=U.z}function u(){let A=new y;for(let U=0;U<r.length;U+=3){A.x=r[U+0],A.y=r[U+1],A.z=r[U+2];let T=g(A)/2/Math.PI+.5,I=m(A)/Math.PI+.5;o.push(T,1-I)}x(),d()}function d(){for(let A=0;A<o.length;A+=6){let U=o[A+0],T=o[A+2],I=o[A+4],L=Math.max(U,T,I),P=Math.min(U,T,I);L>.9&&P<.1&&(U<.2&&(o[A+0]+=1),T<.2&&(o[A+2]+=1),I<.2&&(o[A+4]+=1))}}function f(A){r.push(A.x,A.y,A.z)}function p(A,U){let T=A*3;U.x=e[T+0],U.y=e[T+1],U.z=e[T+2]}function x(){let A=new y,U=new y,T=new y,I=new y,L=new Pe,P=new Pe,M=new Pe;for(let C=0,O=0;C<r.length;C+=9,O+=6){A.set(r[C+0],r[C+1],r[C+2]),U.set(r[C+3],r[C+4],r[C+5]),T.set(r[C+6],r[C+7],r[C+8]),L.set(o[O+0],o[O+1]),P.set(o[O+2],o[O+3]),M.set(o[O+4],o[O+5]),I.copy(A).add(U).add(T).divideScalar(3);let H=g(I);b(L,O+0,A,H),b(P,O+2,U,H),b(M,O+4,T,H)}}function b(A,U,T,I){I<0&&A.x===1&&(o[U]=A.x-1),T.x===0&&T.z===0&&(o[U]=I/2/Math.PI+.5)}function g(A){return Math.atan2(A.z,-A.x)}function m(A){return Math.atan2(-A.y,Math.sqrt(A.x*A.x+A.z*A.z))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.vertices,e.indices,e.radius,e.detail)}};var Ic=new y,Pc=new y,rd=new y,Lc=new gs,ol=class extends tn{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){let s=Math.pow(10,4),r=Math.cos(Vo*t),o=e.getIndex(),a=e.getAttribute("position"),c=o?o.count:a.count,l=[0,0,0],u=["a","b","c"],d=new Array(3),f={},p=[];for(let x=0;x<c;x+=3){o?(l[0]=o.getX(x),l[1]=o.getX(x+1),l[2]=o.getX(x+2)):(l[0]=x,l[1]=x+1,l[2]=x+2);let{a:b,b:g,c:m}=Lc;if(b.fromBufferAttribute(a,l[0]),g.fromBufferAttribute(a,l[1]),m.fromBufferAttribute(a,l[2]),Lc.getNormal(rd),d[0]=`${Math.round(b.x*s)},${Math.round(b.y*s)},${Math.round(b.z*s)}`,d[1]=`${Math.round(g.x*s)},${Math.round(g.y*s)},${Math.round(g.z*s)}`,d[2]=`${Math.round(m.x*s)},${Math.round(m.y*s)},${Math.round(m.z*s)}`,!(d[0]===d[1]||d[1]===d[2]||d[2]===d[0]))for(let A=0;A<3;A++){let U=(A+1)%3,T=d[A],I=d[U],L=Lc[u[A]],P=Lc[u[U]],M=`${T}_${I}`,C=`${I}_${T}`;C in f&&f[C]?(rd.dot(f[C].normal)<=r&&(p.push(L.x,L.y,L.z),p.push(P.x,P.y,P.z)),f[C]=null):M in f||(f[M]={index0:l[A],index1:l[U],normal:rd.clone()})}}for(let x in f)if(f[x]){let{index0:b,index1:g}=f[x];Ic.fromBufferAttribute(a,b),Pc.fromBufferAttribute(a,g),p.push(Ic.x,Ic.y,Ic.z),p.push(Pc.x,Pc.y,Pc.z)}this.setAttribute("position",new Dt(p,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}},Mi=class{constructor(){this.type="Curve",this.arcLengthDivisions=200,this.needsUpdate=!1,this.cacheArcLengths=null}getPoint(){nt("Curve: .getPoint() not implemented.")}getPointAt(e,t){let i=this.getUtoTmapping(e);return this.getPoint(i,t)}getPoints(e=5){let t=[];for(let i=0;i<=e;i++)t.push(this.getPoint(i/e));return t}getSpacedPoints(e=5){let t=[];for(let i=0;i<=e;i++)t.push(this.getPointAt(i/e));return t}getLength(){let e=this.getLengths();return e[e.length-1]}getLengths(e=this.arcLengthDivisions){if(this.cacheArcLengths&&this.cacheArcLengths.length===e+1&&!this.needsUpdate)return this.cacheArcLengths;this.needsUpdate=!1;let t=[],i,s=this.getPoint(0),r=0;t.push(0);for(let o=1;o<=e;o++)i=this.getPoint(o/e),r+=i.distanceTo(s),t.push(r),s=i;return this.cacheArcLengths=t,t}updateArcLengths(){this.needsUpdate=!0,this.getLengths()}getUtoTmapping(e,t=null){let i=this.getLengths(),s=0,r=i.length,o;t?o=t:o=e*i[r-1];let a=0,c=r-1,l;for(;a<=c;)if(s=Math.floor(a+(c-a)/2),l=i[s]-o,l<0)a=s+1;else if(l>0)c=s-1;else{c=s;break}if(s=c,i[s]===o)return s/(r-1);let u=i[s],f=i[s+1]-u,p=(o-u)/f;return(s+p)/(r-1)}getTangent(e,t){let s=e-1e-4,r=e+1e-4;s<0&&(s=0),r>1&&(r=1);let o=this.getPoint(s),a=this.getPoint(r),c=t||(o.isVector2?new Pe:new y);return c.copy(a).sub(o).normalize(),c}getTangentAt(e,t){let i=this.getUtoTmapping(e);return this.getTangent(i,t)}computeFrenetFrames(e,t=!1){let i=new y,s=[],r=[],o=[],a=new y,c=new rt;for(let p=0;p<=e;p++){let x=p/e;s[p]=this.getTangentAt(x,new y)}r[0]=new y,o[0]=new y;let l=Number.MAX_VALUE,u=Math.abs(s[0].x),d=Math.abs(s[0].y),f=Math.abs(s[0].z);u<=l&&(l=u,i.set(1,0,0)),d<=l&&(l=d,i.set(0,1,0)),f<=l&&i.set(0,0,1),a.crossVectors(s[0],i).normalize(),r[0].crossVectors(s[0],a),o[0].crossVectors(s[0],r[0]);for(let p=1;p<=e;p++){if(r[p]=r[p-1].clone(),o[p]=o[p-1].clone(),a.crossVectors(s[p-1],s[p]),a.length()>Number.EPSILON){a.normalize();let x=Math.acos(St(s[p-1].dot(s[p]),-1,1));r[p].applyMatrix4(c.makeRotationAxis(a,x))}o[p].crossVectors(s[p],r[p])}if(t===!0){let p=Math.acos(St(r[0].dot(r[e]),-1,1));p/=e,s[0].dot(a.crossVectors(r[0],r[e]))>0&&(p=-p);for(let x=1;x<=e;x++)r[x].applyMatrix4(c.makeRotationAxis(s[x],p*x)),o[x].crossVectors(s[x],r[x])}return{tangents:s,normals:r,binormals:o}}clone(){return new this.constructor().copy(this)}copy(e){return this.arcLengthDivisions=e.arcLengthDivisions,this}toJSON(){let e={metadata:{version:4.7,type:"Curve",generator:"Curve.toJSON"}};return e.arcLengthDivisions=this.arcLengthDivisions,e.type=this.type,e}fromJSON(e){return this.arcLengthDivisions=e.arcLengthDivisions,this}},al=class extends Mi{constructor(e=0,t=0,i=1,s=1,r=0,o=Math.PI*2,a=!1,c=0){super(),this.isEllipseCurve=!0,this.type="EllipseCurve",this.aX=e,this.aY=t,this.xRadius=i,this.yRadius=s,this.aStartAngle=r,this.aEndAngle=o,this.aClockwise=a,this.aRotation=c}getPoint(e,t=new Pe){let i=t,s=Math.PI*2,r=this.aEndAngle-this.aStartAngle,o=Math.abs(r)<Number.EPSILON;for(;r<0;)r+=s;for(;r>s;)r-=s;r<Number.EPSILON&&(o?r=0:r=s),this.aClockwise===!0&&!o&&(r===s?r=-s:r=r-s);let a=this.aStartAngle+e*r,c=this.aX+this.xRadius*Math.cos(a),l=this.aY+this.yRadius*Math.sin(a);if(this.aRotation!==0){let u=Math.cos(this.aRotation),d=Math.sin(this.aRotation),f=c-this.aX,p=l-this.aY;c=f*u-p*d+this.aX,l=f*d+p*u+this.aY}return i.set(c,l)}copy(e){return super.copy(e),this.aX=e.aX,this.aY=e.aY,this.xRadius=e.xRadius,this.yRadius=e.yRadius,this.aStartAngle=e.aStartAngle,this.aEndAngle=e.aEndAngle,this.aClockwise=e.aClockwise,this.aRotation=e.aRotation,this}toJSON(){let e=super.toJSON();return e.aX=this.aX,e.aY=this.aY,e.xRadius=this.xRadius,e.yRadius=this.yRadius,e.aStartAngle=this.aStartAngle,e.aEndAngle=this.aEndAngle,e.aClockwise=this.aClockwise,e.aRotation=this.aRotation,e}fromJSON(e){return super.fromJSON(e),this.aX=e.aX,this.aY=e.aY,this.xRadius=e.xRadius,this.yRadius=e.yRadius,this.aStartAngle=e.aStartAngle,this.aEndAngle=e.aEndAngle,this.aClockwise=e.aClockwise,this.aRotation=e.aRotation,this}},Jc=class extends al{constructor(e,t,i,s,r,o){super(e,t,i,i,s,r,o),this.isArcCurve=!0,this.type="ArcCurve"}};function $d(){let n=0,e=0,t=0,i=0;function s(r,o,a,c){n=r,e=a,t=-3*r+3*o-2*a-c,i=2*r-2*o+a+c}return{initCatmullRom:function(r,o,a,c,l){s(o,a,l*(a-r),l*(c-o))},initNonuniformCatmullRom:function(r,o,a,c,l,u,d){let f=(o-r)/l-(a-r)/(l+u)+(a-o)/u,p=(a-o)/u-(c-o)/(u+d)+(c-a)/d;f*=u,p*=u,s(o,a,f,p)},calc:function(r){let o=r*r,a=o*r;return n+e*r+t*o+i*a}}}var cm=new y,hm=new y,od=new $d,ad=new $d,ld=new $d,Qc=class extends Mi{constructor(e=[],t=!1,i="centripetal",s=.5){super(),this.isCatmullRomCurve3=!0,this.type="CatmullRomCurve3",this.points=e,this.closed=t,this.curveType=i,this.tension=s}getPoint(e,t=new y){let i=t,s=this.points,r=s.length,o=(r-(this.closed?0:1))*e,a=Math.floor(o),c=o-a;this.closed?a+=a>0?0:(Math.floor(Math.abs(a)/r)+1)*r:c===0&&a===r-1&&(a=r-2,c=1);let l,u;this.closed||a>0?l=s[(a-1)%r]:(hm.subVectors(s[0],s[1]).add(s[0]),l=hm);let d=s[a%r],f=s[(a+1)%r];if(this.closed||a+2<r?u=s[(a+2)%r]:(cm.subVectors(s[r-1],s[r-2]).add(s[r-1]),u=cm),this.curveType==="centripetal"||this.curveType==="chordal"){let p=this.curveType==="chordal"?.5:.25,x=Math.pow(l.distanceToSquared(d),p),b=Math.pow(d.distanceToSquared(f),p),g=Math.pow(f.distanceToSquared(u),p);b<1e-4&&(b=1),x<1e-4&&(x=b),g<1e-4&&(g=b),od.initNonuniformCatmullRom(l.x,d.x,f.x,u.x,x,b,g),ad.initNonuniformCatmullRom(l.y,d.y,f.y,u.y,x,b,g),ld.initNonuniformCatmullRom(l.z,d.z,f.z,u.z,x,b,g)}else this.curveType==="catmullrom"&&(od.initCatmullRom(l.x,d.x,f.x,u.x,this.tension),ad.initCatmullRom(l.y,d.y,f.y,u.y,this.tension),ld.initCatmullRom(l.z,d.z,f.z,u.z,this.tension));return i.set(od.calc(c),ad.calc(c),ld.calc(c)),i}copy(e){super.copy(e),this.points=[];for(let t=0,i=e.points.length;t<i;t++){let s=e.points[t];this.points.push(s.clone())}return this.closed=e.closed,this.curveType=e.curveType,this.tension=e.tension,this}toJSON(){let e=super.toJSON();e.points=[];for(let t=0,i=this.points.length;t<i;t++){let s=this.points[t];e.points.push(s.toArray())}return e.closed=this.closed,e.curveType=this.curveType,e.tension=this.tension,e}fromJSON(e){super.fromJSON(e),this.points=[];for(let t=0,i=e.points.length;t<i;t++){let s=e.points[t];this.points.push(new y().fromArray(s))}return this.closed=e.closed,this.curveType=e.curveType,this.tension=e.tension,this}};function um(n,e,t,i,s){let r=(i-e)*.5,o=(s-t)*.5,a=n*n,c=n*a;return(2*t-2*i+r+o)*c+(-3*t+3*i-2*r-o)*a+r*n+t}function F_(n,e){let t=1-n;return t*t*e}function O_(n,e){return 2*(1-n)*n*e}function B_(n,e){return n*n*e}function $a(n,e,t,i){return F_(n,e)+O_(n,t)+B_(n,i)}function H_(n,e){let t=1-n;return t*t*t*e}function k_(n,e){let t=1-n;return 3*t*t*n*e}function V_(n,e){return 3*(1-n)*n*n*e}function z_(n,e){return n*n*n*e}function Za(n,e,t,i,s){return H_(n,e)+k_(n,t)+V_(n,i)+z_(n,s)}var eh=class extends Mi{constructor(e=new Pe,t=new Pe,i=new Pe,s=new Pe){super(),this.isCubicBezierCurve=!0,this.type="CubicBezierCurve",this.v0=e,this.v1=t,this.v2=i,this.v3=s}getPoint(e,t=new Pe){let i=t,s=this.v0,r=this.v1,o=this.v2,a=this.v3;return i.set(Za(e,s.x,r.x,o.x,a.x),Za(e,s.y,r.y,o.y,a.y)),i}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this.v3.copy(e.v3),this}toJSON(){let e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e.v3=this.v3.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this.v3.fromArray(e.v3),this}},ta=class extends Mi{constructor(e=new y,t=new y,i=new y,s=new y){super(),this.isCubicBezierCurve3=!0,this.type="CubicBezierCurve3",this.v0=e,this.v1=t,this.v2=i,this.v3=s}getPoint(e,t=new y){let i=t,s=this.v0,r=this.v1,o=this.v2,a=this.v3;return i.set(Za(e,s.x,r.x,o.x,a.x),Za(e,s.y,r.y,o.y,a.y),Za(e,s.z,r.z,o.z,a.z)),i}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this.v3.copy(e.v3),this}toJSON(){let e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e.v3=this.v3.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this.v3.fromArray(e.v3),this}},th=class extends Mi{constructor(e=new Pe,t=new Pe){super(),this.isLineCurve=!0,this.type="LineCurve",this.v1=e,this.v2=t}getPoint(e,t=new Pe){let i=t;return e===1?i.copy(this.v2):(i.copy(this.v2).sub(this.v1),i.multiplyScalar(e).add(this.v1)),i}getPointAt(e,t){return this.getPoint(e,t)}getTangent(e,t=new Pe){return t.subVectors(this.v2,this.v1).normalize()}getTangentAt(e,t){return this.getTangent(e,t)}copy(e){return super.copy(e),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){let e=super.toJSON();return e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}},Zr=class extends Mi{constructor(e=new y,t=new y){super(),this.isLineCurve3=!0,this.type="LineCurve3",this.v1=e,this.v2=t}getPoint(e,t=new y){let i=t;return e===1?i.copy(this.v2):(i.copy(this.v2).sub(this.v1),i.multiplyScalar(e).add(this.v1)),i}getPointAt(e,t){return this.getPoint(e,t)}getTangent(e,t=new y){return t.subVectors(this.v2,this.v1).normalize()}getTangentAt(e,t){return this.getTangent(e,t)}copy(e){return super.copy(e),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){let e=super.toJSON();return e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}},nh=class extends Mi{constructor(e=new Pe,t=new Pe,i=new Pe){super(),this.isQuadraticBezierCurve=!0,this.type="QuadraticBezierCurve",this.v0=e,this.v1=t,this.v2=i}getPoint(e,t=new Pe){let i=t,s=this.v0,r=this.v1,o=this.v2;return i.set($a(e,s.x,r.x,o.x),$a(e,s.y,r.y,o.y)),i}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){let e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}},Kr=class extends Mi{constructor(e=new y,t=new y,i=new y){super(),this.isQuadraticBezierCurve3=!0,this.type="QuadraticBezierCurve3",this.v0=e,this.v1=t,this.v2=i}getPoint(e,t=new y){let i=t,s=this.v0,r=this.v1,o=this.v2;return i.set($a(e,s.x,r.x,o.x),$a(e,s.y,r.y,o.y),$a(e,s.z,r.z,o.z)),i}copy(e){return super.copy(e),this.v0.copy(e.v0),this.v1.copy(e.v1),this.v2.copy(e.v2),this}toJSON(){let e=super.toJSON();return e.v0=this.v0.toArray(),e.v1=this.v1.toArray(),e.v2=this.v2.toArray(),e}fromJSON(e){return super.fromJSON(e),this.v0.fromArray(e.v0),this.v1.fromArray(e.v1),this.v2.fromArray(e.v2),this}},ih=class extends Mi{constructor(e=[]){super(),this.isSplineCurve=!0,this.type="SplineCurve",this.points=e}getPoint(e,t=new Pe){let i=t,s=this.points,r=(s.length-1)*e,o=Math.floor(r),a=r-o,c=s[o===0?o:o-1],l=s[o],u=s[o>s.length-2?s.length-1:o+1],d=s[o>s.length-3?s.length-1:o+2];return i.set(um(a,c.x,l.x,u.x,d.x),um(a,c.y,l.y,u.y,d.y)),i}copy(e){super.copy(e),this.points=[];for(let t=0,i=e.points.length;t<i;t++){let s=e.points[t];this.points.push(s.clone())}return this}toJSON(){let e=super.toJSON();e.points=[];for(let t=0,i=this.points.length;t<i;t++){let s=this.points[t];e.points.push(s.toArray())}return e}fromJSON(e){super.fromJSON(e),this.points=[];for(let t=0,i=e.points.length;t<i;t++){let s=e.points[t];this.points.push(new Pe().fromArray(s))}return this}},_d=Object.freeze({__proto__:null,ArcCurve:Jc,CatmullRomCurve3:Qc,CubicBezierCurve:eh,CubicBezierCurve3:ta,EllipseCurve:al,LineCurve:th,LineCurve3:Zr,QuadraticBezierCurve:nh,QuadraticBezierCurve3:Kr,SplineCurve:ih}),ll=class extends Mi{constructor(){super(),this.type="CurvePath",this.curves=[],this.autoClose=!1}add(e){this.curves.push(e)}closePath(){let e=this.curves[0].getPoint(0),t=this.curves[this.curves.length-1].getPoint(1);if(!e.equals(t)){let i=e.isVector2===!0?"LineCurve":"LineCurve3";this.curves.push(new _d[i](t,e))}return this}getPoint(e,t){let i=e*this.getLength(),s=this.getCurveLengths(),r=0;for(;r<s.length;){if(s[r]>=i){let o=s[r]-i,a=this.curves[r],c=a.getLength(),l=c===0?0:1-o/c;return a.getPointAt(l,t)}r++}return null}getLength(){let e=this.getCurveLengths();return e[e.length-1]}updateArcLengths(){this.needsUpdate=!0,this.cacheLengths=null,this.getCurveLengths()}getCurveLengths(){if(this.cacheLengths&&this.cacheLengths.length===this.curves.length)return this.cacheLengths;let e=[],t=0;for(let i=0,s=this.curves.length;i<s;i++)t+=this.curves[i].getLength(),e.push(t);return this.cacheLengths=e,e}getSpacedPoints(e=40){let t=[];for(let i=0;i<=e;i++)t.push(this.getPoint(i/e));return this.autoClose&&t.push(t[0]),t}getPoints(e=12){let t=[],i;for(let s=0,r=this.curves;s<r.length;s++){let o=r[s],a=o.isEllipseCurve?e*2:o.isLineCurve||o.isLineCurve3?1:o.isSplineCurve?e*o.points.length:e,c=o.getPoints(a);for(let l=0;l<c.length;l++){let u=c[l];i&&i.equals(u)||(t.push(u),i=u)}}return this.autoClose&&t.length>1&&!t[t.length-1].equals(t[0])&&t.push(t[0]),t}copy(e){super.copy(e),this.curves=[];for(let t=0,i=e.curves.length;t<i;t++){let s=e.curves[t];this.curves.push(s.clone())}return this.autoClose=e.autoClose,this}toJSON(){let e=super.toJSON();e.autoClose=this.autoClose,e.curves=[];for(let t=0,i=this.curves.length;t<i;t++){let s=this.curves[t];e.curves.push(s.toJSON())}return e}fromJSON(e){super.fromJSON(e),this.autoClose=e.autoClose,this.curves=[];for(let t=0,i=e.curves.length;t<i;t++){let s=e.curves[t];this.curves.push(new _d[s.type]().fromJSON(s))}return this}};var cl=class n extends jc{constructor(e=1,t=0){let i=(1+Math.sqrt(5))/2,s=[-1,i,0,1,i,0,-1,-i,0,1,-i,0,0,-1,i,0,1,i,0,-1,-i,0,1,-i,i,0,-1,i,0,1,-i,0,-1,-i,0,1],r=[0,11,5,0,5,1,0,1,7,0,7,10,0,10,11,1,5,9,5,11,4,11,10,2,10,7,6,7,1,8,3,9,4,3,4,2,3,2,6,3,6,8,3,8,9,4,9,5,2,4,11,6,2,10,8,6,7,9,8,1];super(s,r,e,t),this.type="IcosahedronGeometry",this.parameters={radius:e,detail:t}}static fromJSON(e){return new n(e.radius,e.detail)}};var cn=class n extends tn{constructor(e=1,t=1,i=1,s=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:s};let r=e/2,o=t/2,a=Math.floor(i),c=Math.floor(s),l=a+1,u=c+1,d=e/a,f=t/c,p=[],x=[],b=[],g=[];for(let m=0;m<u;m++){let A=m*f-o;for(let U=0;U<l;U++){let T=U*d-r;x.push(T,-A,0),b.push(0,0,1),g.push(U/a),g.push(1-m/c)}}for(let m=0;m<c;m++)for(let A=0;A<a;A++){let U=A+l*m,T=A+l*(m+1),I=A+1+l*(m+1),L=A+1+l*m;p.push(U,T,L),p.push(T,I,L)}this.setIndex(p),this.setAttribute("position",new Dt(x,3)),this.setAttribute("normal",new Dt(b,3)),this.setAttribute("uv",new Dt(g,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.width,e.height,e.widthSegments,e.heightSegments)}};var Ei=class n extends tn{constructor(e=1,t=32,i=16,s=0,r=Math.PI*2,o=0,a=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:s,phiLength:r,thetaStart:o,thetaLength:a},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));let c=Math.min(o+a,Math.PI),l=0,u=[],d=new y,f=new y,p=[],x=[],b=[],g=[];for(let m=0;m<=i;m++){let A=[],U=m/i,T=o+U*a,I=e*Math.cos(T),L=Math.sqrt(e*e-I*I),P=0;m===0&&o===0?P=.5/t:m===i&&c===Math.PI&&(P=-.5/t);for(let M=0;M<=t;M++){let C=M/t,O=s+C*r;d.x=-L*Math.cos(O),d.y=I,d.z=L*Math.sin(O),x.push(d.x,d.y,d.z),f.copy(d).normalize(),b.push(f.x,f.y,f.z),g.push(C+P,1-U),A.push(l++)}u.push(A)}for(let m=0;m<i;m++)for(let A=0;A<t;A++){let U=u[m][A+1],T=u[m][A],I=u[m+1][A],L=u[m+1][A+1];(m!==0||o>0)&&p.push(U,T,L),(m!==i-1||c<Math.PI)&&p.push(T,I,L)}this.setIndex(p),this.setAttribute("position",new Dt(x,3)),this.setAttribute("normal",new Dt(b,3)),this.setAttribute("uv",new Dt(g,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}};var bi=class n extends tn{constructor(e=1,t=.4,i=12,s=48,r=Math.PI*2,o=0,a=Math.PI*2){super(),this.type="TorusGeometry",this.parameters={radius:e,tube:t,radialSegments:i,tubularSegments:s,arc:r,thetaStart:o,thetaLength:a},i=Math.floor(i),s=Math.floor(s);let c=[],l=[],u=[],d=[],f=new y,p=new y,x=new y;for(let b=0;b<=i;b++){let g=o+b/i*a;for(let m=0;m<=s;m++){let A=m/s*r;p.x=(e+t*Math.cos(g))*Math.cos(A),p.y=(e+t*Math.cos(g))*Math.sin(A),p.z=t*Math.sin(g),l.push(p.x,p.y,p.z),f.x=e*Math.cos(A),f.y=e*Math.sin(A),x.subVectors(p,f).normalize(),u.push(x.x,x.y,x.z),d.push(m/s),d.push(b/i)}}for(let b=1;b<=i;b++)for(let g=1;g<=s;g++){let m=(s+1)*b+g-1,A=(s+1)*(b-1)+g-1,U=(s+1)*(b-1)+g,T=(s+1)*b+g;c.push(m,A,T),c.push(A,U,T)}this.setIndex(c),this.setAttribute("position",new Dt(l,3)),this.setAttribute("normal",new Dt(u,3)),this.setAttribute("uv",new Dt(d,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radius,e.tube,e.radialSegments,e.tubularSegments,e.arc,e.thetaStart,e.thetaLength)}};var jr=class n extends tn{constructor(e=new Kr(new y(-1,-1,0),new y(-1,1,0),new y(1,1,0)),t=64,i=1,s=8,r=!1){super(),this.type="TubeGeometry",this.parameters={path:e,tubularSegments:t,radius:i,radialSegments:s,closed:r};let o=e.computeFrenetFrames(t,r);this.tangents=o.tangents,this.normals=o.normals,this.binormals=o.binormals;let a=new y,c=new y,l=new Pe,u=new y,d=[],f=[],p=[],x=[];b(),this.setIndex(x),this.setAttribute("position",new Dt(d,3)),this.setAttribute("normal",new Dt(f,3)),this.setAttribute("uv",new Dt(p,2));function b(){for(let U=0;U<t;U++)g(U);g(r===!1?t:0),A(),m()}function g(U){u=e.getPointAt(U/t,u);let T=o.normals[U],I=o.binormals[U];for(let L=0;L<=s;L++){let P=L/s*Math.PI*2,M=Math.sin(P),C=-Math.cos(P);c.x=C*T.x+M*I.x,c.y=C*T.y+M*I.y,c.z=C*T.z+M*I.z,c.normalize(),f.push(c.x,c.y,c.z),a.x=u.x+i*c.x,a.y=u.y+i*c.y,a.z=u.z+i*c.z,d.push(a.x,a.y,a.z)}}function m(){for(let U=1;U<=t;U++)for(let T=1;T<=s;T++){let I=(s+1)*(U-1)+(T-1),L=(s+1)*U+(T-1),P=(s+1)*U+T,M=(s+1)*(U-1)+T;x.push(I,L,M),x.push(L,P,M)}}function A(){for(let U=0;U<=t;U++)for(let T=0;T<=s;T++)l.x=U/t,l.y=T/s,p.push(l.x,l.y)}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}toJSON(){let e=super.toJSON();return e.path=this.parameters.path.toJSON(),e}static fromJSON(e){return new n(new _d[e.path.type]().fromJSON(e.path),e.tubularSegments,e.radius,e.radialSegments,e.closed)}};function io(n){let e={};for(let t in n){e[t]={};for(let i in n[t]){let s=n[t][i];if(dm(s))s.isRenderTargetTexture?(nt("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=s.clone();else if(Array.isArray(s))if(dm(s[0])){let r=[];for(let o=0,a=s.length;o<a;o++)r[o]=s[o].clone();e[t][i]=r}else e[t][i]=s.slice();else e[t][i]=s}}return e}function $n(n){let e={};for(let t=0;t<n.length;t++){let i=io(n[t]);for(let s in i)e[s]=i[s]}return e}function dm(n){return n&&(n.isColor||n.isMatrix3||n.isMatrix4||n.isVector2||n.isVector3||n.isVector4||n.isTexture||n.isQuaternion)}function G_(n){let e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function Zd(n){let e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:It.workingColorSpace}var ou={clone:io,merge:$n},W_=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,X_=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`,Un=class extends ni{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=W_,this.fragmentShader=X_,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=io(e.uniforms),this.uniformsGroups=G_(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this.defaultAttributeValues=Object.assign({},e.defaultAttributeValues),this.index0AttributeName=e.index0AttributeName,this.uniformsNeedUpdate=e.uniformsNeedUpdate,this}toJSON(e){let t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(let s in this.uniforms){let o=this.uniforms[s].value;o&&o.isTexture?t.uniforms[s]={type:"t",value:o.toJSON(e).uuid}:o&&o.isColor?t.uniforms[s]={type:"c",value:o.getHex()}:o&&o.isVector2?t.uniforms[s]={type:"v2",value:o.toArray()}:o&&o.isVector3?t.uniforms[s]={type:"v3",value:o.toArray()}:o&&o.isVector4?t.uniforms[s]={type:"v4",value:o.toArray()}:o&&o.isMatrix3?t.uniforms[s]={type:"m3",value:o.toArray()}:o&&o.isMatrix4?t.uniforms[s]={type:"m4",value:o.toArray()}:t.uniforms[s]={value:o}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;let i={};for(let s in this.extensions)this.extensions[s]===!0&&(i[s]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}fromJSON(e,t){if(super.fromJSON(e,t),e.uniforms!==void 0)for(let i in e.uniforms){let s=e.uniforms[i];switch(this.uniforms[i]={},s.type){case"t":this.uniforms[i].value=t[s.value]||null;break;case"c":this.uniforms[i].value=new ke().setHex(s.value);break;case"v2":this.uniforms[i].value=new Pe().fromArray(s.value);break;case"v3":this.uniforms[i].value=new y().fromArray(s.value);break;case"v4":this.uniforms[i].value=new $t().fromArray(s.value);break;case"m3":this.uniforms[i].value=new gt().fromArray(s.value);break;case"m4":this.uniforms[i].value=new rt().fromArray(s.value);break;default:this.uniforms[i].value=s.value}}if(e.defines!==void 0&&(this.defines=e.defines),e.vertexShader!==void 0&&(this.vertexShader=e.vertexShader),e.fragmentShader!==void 0&&(this.fragmentShader=e.fragmentShader),e.glslVersion!==void 0&&(this.glslVersion=e.glslVersion),e.extensions!==void 0)for(let i in e.extensions)this.extensions[i]=e.extensions[i];return e.lights!==void 0&&(this.lights=e.lights),e.clipping!==void 0&&(this.clipping=e.clipping),this}},sh=class extends Un{constructor(e){super(e),this.isRawShaderMaterial=!0,this.type="RawShaderMaterial"}},ge=class extends ni{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new ke(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ke(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=iu,this.normalScale=new Pe(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Pi,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}},hi=class extends ge{constructor(e){super(),this.isMeshPhysicalMaterial=!0,this.defines={STANDARD:"",PHYSICAL:""},this.type="MeshPhysicalMaterial",this.anisotropyRotation=0,this.anisotropyMap=null,this.clearcoatMap=null,this.clearcoatRoughness=0,this.clearcoatRoughnessMap=null,this.clearcoatNormalScale=new Pe(1,1),this.clearcoatNormalMap=null,this.ior=1.5,Object.defineProperty(this,"reflectivity",{get:function(){return St(2.5*(this.ior-1)/(this.ior+1),0,1)},set:function(t){this.ior=(1+.4*t)/(1-.4*t)}}),this.iridescenceMap=null,this.iridescenceIOR=1.3,this.iridescenceThicknessRange=[100,400],this.iridescenceThicknessMap=null,this.sheenColor=new ke(0),this.sheenColorMap=null,this.sheenRoughness=1,this.sheenRoughnessMap=null,this.transmissionMap=null,this.thickness=0,this.thicknessMap=null,this.attenuationDistance=1/0,this.attenuationColor=new ke(1,1,1),this.specularIntensity=1,this.specularIntensityMap=null,this.specularColor=new ke(1,1,1),this.specularColorMap=null,this._anisotropy=0,this._clearcoat=0,this._dispersion=0,this._iridescence=0,this._retroreflectivity=0,this._sheen=0,this._transmission=0,this.setValues(e)}get anisotropy(){return this._anisotropy}set anisotropy(e){this._anisotropy>0!=e>0&&this.version++,this._anisotropy=e}get clearcoat(){return this._clearcoat}set clearcoat(e){this._clearcoat>0!=e>0&&this.version++,this._clearcoat=e}get iridescence(){return this._iridescence}set iridescence(e){this._iridescence>0!=e>0&&this.version++,this._iridescence=e}get dispersion(){return this._dispersion}set dispersion(e){this._dispersion>0!=e>0&&this.version++,this._dispersion=e}get retroreflectivity(){return this._retroreflectivity}set retroreflectivity(e){this._retroreflectivity>0!=e>0&&this.version++,this._retroreflectivity=e}get sheen(){return this._sheen}set sheen(e){this._sheen>0!=e>0&&this.version++,this._sheen=e}get transmission(){return this._transmission}set transmission(e){this._transmission>0!=e>0&&this.version++,this._transmission=e}copy(e){return super.copy(e),this.defines={STANDARD:"",PHYSICAL:""},this.anisotropy=e.anisotropy,this.anisotropyRotation=e.anisotropyRotation,this.anisotropyMap=e.anisotropyMap,this.clearcoat=e.clearcoat,this.clearcoatMap=e.clearcoatMap,this.clearcoatRoughness=e.clearcoatRoughness,this.clearcoatRoughnessMap=e.clearcoatRoughnessMap,this.clearcoatNormalMap=e.clearcoatNormalMap,this.clearcoatNormalScale.copy(e.clearcoatNormalScale),this.dispersion=e.dispersion,this.ior=e.ior,this.iridescence=e.iridescence,this.iridescenceMap=e.iridescenceMap,this.iridescenceIOR=e.iridescenceIOR,this.iridescenceThicknessRange=[...e.iridescenceThicknessRange],this.iridescenceThicknessMap=e.iridescenceThicknessMap,this.retroreflectivity=e.retroreflectivity,this.sheen=e.sheen,this.sheenColor.copy(e.sheenColor),this.sheenColorMap=e.sheenColorMap,this.sheenRoughness=e.sheenRoughness,this.sheenRoughnessMap=e.sheenRoughnessMap,this.transmission=e.transmission,this.transmissionMap=e.transmissionMap,this.thickness=e.thickness,this.thicknessMap=e.thicknessMap,this.attenuationDistance=e.attenuationDistance,this.attenuationColor.copy(e.attenuationColor),this.specularIntensity=e.specularIntensity,this.specularIntensityMap=e.specularIntensityMap,this.specularColor.copy(e.specularColor),this.specularColorMap=e.specularColorMap,this}};var rh=class extends ni{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=qm,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}},oh=class extends ni{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}};function lr(n,e){return!n||n.constructor===e?n:typeof e.BYTES_PER_ELEMENT=="number"?new e(n):Array.prototype.slice.call(n)}function Oc(n){return n!==void 0&&n.inTangents!==void 0&&n.outTangents!==void 0}function q_(n){function e(s,r){return n[s]-n[r]}let t=n.length,i=new Array(t);for(let s=0;s!==t;++s)i[s]=s;return i.sort(e),i}function fm(n,e,t){let i=n.length,s=new n.constructor(i);for(let r=0,o=0;o!==i;++r){let a=t[r]*e;for(let c=0;c!==e;++c)s[o++]=n[a+c]}return s}function Y_(n,e,t,i){let s=1,r=n[0];for(;r!==void 0&&r[i]===void 0;)r=n[s++];if(r===void 0)return;let o=r[i];if(o!==void 0)if(Array.isArray(o))do o=r[i],o!==void 0&&(e.push(r.time),t.push(...o)),r=n[s++];while(r!==void 0);else if(o.toArray!==void 0)do o=r[i],o!==void 0&&(e.push(r.time),o.toArray(t,t.length)),r=n[s++];while(r!==void 0);else do o=r[i],o!==void 0&&(e.push(r.time),t.push(o)),r=n[s++];while(r!==void 0)}var ys=class{constructor(e,t,i,s){this.parameterPositions=e,this._cachedIndex=0,this.resultBuffer=s!==void 0?s:new t.constructor(i),this.sampleValues=t,this.valueSize=i,this.settings=null,this.DefaultSettings_={}}evaluate(e){let t=this.parameterPositions,i=this._cachedIndex,s=t[i],r=t[i-1];n:{e:{let o;t:{i:if(!(e<s)){for(let a=i+2;;){if(s===void 0){if(e<r)break i;return i=t.length,this._cachedIndex=i,this.copySampleValue_(i-1)}if(i===a)break;if(r=s,s=t[++i],e<s)break e}o=t.length;break t}if(!(e>=r)){let a=t[1];e<a&&(i=2,r=a);for(let c=i-2;;){if(r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(i===c)break;if(s=r,r=t[--i-1],e>=r)break e}o=i,i=0;break t}break n}for(;i<o;){let a=i+o>>>1;e<t[a]?o=a:i=a+1}if(s=t[i],r=t[i-1],r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(s===void 0)return i=t.length,this._cachedIndex=i,this.copySampleValue_(i-1)}this._cachedIndex=i,this.intervalChanged_(i,r,s)}return this.interpolate_(i,r,e,s)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(e){let t=this.resultBuffer,i=this.sampleValues,s=this.valueSize,r=e*s;for(let o=0;o!==s;++o)t[o]=i[r+o];return t}interpolate_(){throw new Error("THREE.Interpolant: Call to abstract method.")}intervalChanged_(){}},ah=class extends ys{constructor(e,t,i,s){super(e,t,i,s),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:fd,endingEnd:fd}}intervalChanged_(e,t,i){let s=this.parameterPositions,r=e-2,o=e+1,a=s[r],c=s[o];if(a===void 0)switch(this.getSettings_().endingStart){case pd:r=e,a=2*t-i;break;case md:r=s.length-2,a=t+s[r]-s[r+1];break;default:r=e,a=i}if(c===void 0)switch(this.getSettings_().endingEnd){case pd:o=e,c=2*i-t;break;case md:o=1,c=i+s[1]-s[0];break;default:o=e-1,c=t}let l=(i-t)*.5,u=this.valueSize;this._weightPrev=l/(t-a),this._weightNext=l/(c-i),this._offsetPrev=r*u,this._offsetNext=o*u}interpolate_(e,t,i,s){let r=this.resultBuffer,o=this.sampleValues,a=this.valueSize,c=e*a,l=c-a,u=this._offsetPrev,d=this._offsetNext,f=this._weightPrev,p=this._weightNext,x=(i-t)/(s-t),b=x*x,g=b*x,m=-f*g+2*f*b-f*x,A=(1+f)*g+(-1.5-2*f)*b+(-.5+f)*x+1,U=(-1-p)*g+(1.5+p)*b+.5*x,T=p*g-p*b;for(let I=0;I!==a;++I)r[I]=m*o[u+I]+A*o[l+I]+U*o[c+I]+T*o[d+I];return r}},lh=class extends ys{constructor(e,t,i,s){super(e,t,i,s)}interpolate_(e,t,i,s){let r=this.resultBuffer,o=this.sampleValues,a=this.valueSize,c=e*a,l=c-a,u=(i-t)/(s-t),d=1-u;for(let f=0;f!==a;++f)r[f]=o[l+f]*d+o[c+f]*u;return r}},ch=class extends ys{constructor(e,t,i,s){super(e,t,i,s)}interpolate_(e){return this.copySampleValue_(e-1)}},hh=class extends ys{interpolate_(e,t,i,s){let r=this.resultBuffer,o=this.sampleValues,a=this.valueSize,c=e*a,l=c-a,u=this.inTangents,d=this.outTangents;if(!u||!d){let x=(i-t)/(s-t),b=1-x;for(let g=0;g!==a;++g)r[g]=o[l+g]*b+o[c+g]*x;return r}let f=a*2,p=e-1;for(let x=0;x!==a;++x){let b=o[l+x],g=o[c+x],m=p*f+x*2,A=d[m],U=d[m+1],T=e*f+x*2,I=u[T],L=u[T+1],P=Z_(i,t,A,I,s);r[x]=a0(P,b,U,L,g)}return r}};function a0(n,e,t,i,s){let r=1-n;return r*r*r*e+3*r*r*n*t+3*r*n*n*i+n*n*n*s}function $_(n,e,t,i,s){let r=1-n;return 3*r*r*(t-e)+6*r*n*(i-t)+3*n*n*(s-i)}function Z_(n,e,t,i,s){let r=(n-e)/(s-e);for(let o=0;o<8;o++){let a=a0(r,e,t,i,s)-n;if(Math.abs(a)<1e-10)break;let c=$_(r,e,t,i,s);if(Math.abs(c)<1e-10)break;r=Math.max(0,Math.min(1,r-a/c))}return r}var ui=class{constructor(e,t,i,s){if(e===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(t===void 0||t.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+e);this.name=e,this.times=lr(t,this.TimeBufferType),this.values=lr(i,this.ValueBufferType),this.setInterpolation(s||this.DefaultInterpolation)}static toJSON(e){let t=e.constructor,i;if(t.toJSON!==this.toJSON)i=t.toJSON(e);else{i={name:e.name,times:lr(e.times,Array),values:lr(e.values,Array)};let s=e.getInterpolation();s!==e.DefaultInterpolation&&(i.interpolation=s),Oc(e.settings)&&(i.settings={inTangents:lr(e.settings.inTangents,Array),outTangents:lr(e.settings.outTangents,Array)})}return i.type=e.ValueTypeName,i}InterpolantFactoryMethodDiscrete(e){return new ch(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodLinear(e){return new lh(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodSmooth(e){return new ah(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodBezier(e){let t=new hh(this.times,this.values,this.getValueSize(),e);return this.settings&&(t.inTangents=this.settings.inTangents,t.outTangents=this.settings.outTangents),t}setInterpolation(e){let t;switch(e){case Vr:t=this.InterpolantFactoryMethodDiscrete;break;case zr:t=this.InterpolantFactoryMethodLinear;break;case Uc:t=this.InterpolantFactoryMethodSmooth;break;case dd:t=this.InterpolantFactoryMethodBezier;break}if(t===void 0){let i="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(e!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(i);return nt("KeyframeTrack:",i),this}return this.createInterpolant=t,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return Vr;case this.InterpolantFactoryMethodLinear:return zr;case this.InterpolantFactoryMethodSmooth:return Uc;case this.InterpolantFactoryMethodBezier:return dd}}getValueSize(){return this.values.length/this.times.length}shift(e){if(e!==0){let t=this.times;for(let i=0,s=t.length;i!==s;++i)t[i]+=e}return this}scale(e){if(e!==1){let t=this.times;for(let i=0,s=t.length;i!==s;++i)t[i]*=e;Oc(this.settings)&&(pm(this.settings.inTangents,e),pm(this.settings.outTangents,e))}return this}trim(e,t){let i=this.times,s=i.length,r=0,o=s-1;for(;r!==s&&i[r]<e;)++r;for(;o!==-1&&i[o]>t;)--o;if(++o,r!==0||o!==s){r>=o&&(o=Math.max(o,1),r=o-1);let a=this.getValueSize();this.times=i.slice(r,o),this.values=this.values.slice(r*a,o*a)}return this}validate(){let e=!0,t=this.getValueSize();t-Math.floor(t)!==0&&(ht("KeyframeTrack: Invalid value size in track.",this),e=!1);let i=this.times,s=this.values,r=i.length;r===0&&(ht("KeyframeTrack: Track is empty.",this),e=!1);let o=null;for(let a=0;a!==r;a++){let c=i[a];if(typeof c=="number"&&isNaN(c)){ht("KeyframeTrack: Time is not a valid number.",this,a,c),e=!1;break}if(o!==null&&o>c){ht("KeyframeTrack: Out of order keys.",this,a,c,o),e=!1;break}o=c}if(s!==void 0&&Jg(s))for(let a=0,c=s.length;a!==c;++a){let l=s[a];if(isNaN(l)){ht("KeyframeTrack: Value is not a valid number.",this,a,l),e=!1;break}}return e}optimize(){let e=this.times.slice(),t=this.values.slice(),i=this.getValueSize(),s=this.getInterpolation()===Uc,r=e.length-1,o=1;for(let a=1;a<r;++a){let c=!1,l=e[a],u=e[a+1];if(l!==u&&(a!==1||l!==e[0]))if(s)c=!0;else{let d=a*i,f=d-i,p=d+i;for(let x=0;x!==i;++x){let b=t[d+x];if(b!==t[f+x]||b!==t[p+x]){c=!0;break}}}if(c){if(a!==o){e[o]=e[a];let d=a*i,f=o*i;for(let p=0;p!==i;++p)t[f+p]=t[d+p]}++o}}if(r>0){e[o]=e[r];for(let a=r*i,c=o*i,l=0;l!==i;++l)t[c+l]=t[a+l];++o}return o!==e.length?(this.times=e.slice(0,o),this.values=t.slice(0,o*i)):(this.times=e,this.values=t),this}clone(){let e=this.times.slice(),t=this.values.slice(),i=this.constructor,s=new i(this.name,e,t);return s.createInterpolant=this.createInterpolant,Oc(this.settings)&&(s.settings={inTangents:this.settings.inTangents.slice(),outTangents:this.settings.outTangents.slice()}),s}};function pm(n,e){for(let t=0,i=n.length;t!==i;t+=2)n[t]*=e}ui.prototype.ValueTypeName="";ui.prototype.TimeBufferType=Float32Array;ui.prototype.ValueBufferType=Float32Array;ui.prototype.DefaultInterpolation=zr;var Gs=class extends ui{constructor(e,t,i){super(e,t,i)}};Gs.prototype.ValueTypeName="bool";Gs.prototype.ValueBufferType=Array;Gs.prototype.DefaultInterpolation=Vr;Gs.prototype.InterpolantFactoryMethodLinear=void 0;Gs.prototype.InterpolantFactoryMethodSmooth=void 0;var hl=class extends ui{constructor(e,t,i,s){super(e,t,i,s)}};hl.prototype.ValueTypeName="color";var Ws=class extends ui{constructor(e,t,i,s){super(e,t,i,s)}};Ws.prototype.ValueTypeName="number";var uh=class extends ys{constructor(e,t,i,s){super(e,t,i,s)}interpolate_(e,t,i,s){let r=this.resultBuffer,o=this.sampleValues,a=this.valueSize,c=(i-t)/(s-t),l=e*a;for(let u=l+a;l!==u;l+=4)rn.slerpFlat(r,0,o,l-a,o,l,c);return r}},Xs=class extends ui{constructor(e,t,i,s){super(e,t,i,s)}InterpolantFactoryMethodLinear(e){return new uh(this.times,this.values,this.getValueSize(),e)}};Xs.prototype.ValueTypeName="quaternion";Xs.prototype.InterpolantFactoryMethodSmooth=void 0;var qs=class extends ui{constructor(e,t,i){super(e,t,i)}};qs.prototype.ValueTypeName="string";qs.prototype.ValueBufferType=Array;qs.prototype.DefaultInterpolation=Vr;qs.prototype.InterpolantFactoryMethodLinear=void 0;qs.prototype.InterpolantFactoryMethodSmooth=void 0;var pr=class extends ui{constructor(e,t,i,s){super(e,t,i,s)}};pr.prototype.ValueTypeName="vector";var ul=class{constructor(e="",t=-1,i=[],s=Xm){this.name=e,this.tracks=i,this.duration=t,this.blendMode=s,this.uuid=Ji(),this.userData={},this.duration<0&&this.resetDuration()}static parse(e){let t=[],i=e.tracks,s=1/(e.fps||1);for(let o=0,a=i.length;o!==a;++o)t.push(j_(i[o]).scale(s));let r=new this(e.name,e.duration,t,e.blendMode);return r.uuid=e.uuid,r.userData=JSON.parse(e.userData||"{}"),r}static toJSON(e){let t=[],i=e.tracks,s={name:e.name,duration:e.duration,tracks:t,uuid:e.uuid,blendMode:e.blendMode,userData:JSON.stringify(e.userData)};for(let r=0,o=i.length;r!==o;++r)t.push(ui.toJSON(i[r]));return s}static CreateFromMorphTargetSequence(e,t,i,s){let r=t.length,o=[];for(let a=0;a<r;a++){let c=[],l=[];c.push((a+r-1)%r,a,(a+1)%r),l.push(0,1,0);let u=q_(c);c=fm(c,1,u),l=fm(l,1,u),!s&&c[0]===0&&(c.push(r),l.push(l[0])),o.push(new Ws(".morphTargetInfluences["+t[a].name+"]",c,l).scale(1/i))}return new this(e,-1,o)}static findByName(e,t){let i=e;if(!Array.isArray(e)){let s=e;i=s.geometry&&s.geometry.animations||s.animations}for(let s=0;s<i.length;s++)if(i[s].name===t)return i[s];return null}static CreateClipsFromMorphTargetSequences(e,t,i){let s={},r=/^([\w-]*?)([\d]+)$/;for(let a=0,c=e.length;a<c;a++){let l=e[a],u=l.name.match(r);if(u&&u.length>1){let d=u[1],f=s[d];f||(s[d]=f=[]),f.push(l)}}let o=[];for(let a in s)o.push(this.CreateFromMorphTargetSequence(a,s[a],t,i));return o}resetDuration(){let e=this.tracks,t=0;for(let i=0,s=e.length;i!==s;++i){let r=this.tracks[i];t=Math.max(t,r.times[r.times.length-1])}return this.duration=t,this}trim(){for(let e=0;e<this.tracks.length;e++)this.tracks[e].trim(0,this.duration);return this}validate(){let e=!0;for(let t=0;t<this.tracks.length;t++)e=e&&this.tracks[t].validate();return e}optimize(){for(let e=0;e<this.tracks.length;e++)this.tracks[e].optimize();return this}clone(){let e=[];for(let i=0;i<this.tracks.length;i++)e.push(this.tracks[i].clone());let t=new this.constructor(this.name,this.duration,e,this.blendMode);return t.userData=JSON.parse(JSON.stringify(this.userData)),t}toJSON(){return this.constructor.toJSON(this)}};function K_(n){switch(n.toLowerCase()){case"scalar":case"double":case"float":case"number":case"integer":return Ws;case"vector":case"vector2":case"vector3":case"vector4":return pr;case"color":return hl;case"quaternion":return Xs;case"bool":case"boolean":return Gs;case"string":return qs}throw new Error("THREE.KeyframeTrack: Unsupported typeName: "+n)}function j_(n){if(n.type===void 0)throw new Error("THREE.KeyframeTrack: track type undefined, can not parse");let e=K_(n.type);if(n.times===void 0){let i=[],s=[];Y_(n.keys,i,s,"value"),n.times=i,n.values=s}let t;return e.parse!==void 0?t=e.parse(n):t=new e(n.name,n.times,n.values,n.interpolation),Oc(n.settings)&&(t.settings={inTangents:lr(n.settings.inTangents,Float32Array),outTangents:lr(n.settings.outTangents,Float32Array)}),t}var _s={enabled:!1,files:{},add:function(n,e){this.enabled!==!1&&(mm(n)||(this.files[n]=e))},get:function(n){if(this.enabled!==!1&&!mm(n))return this.files[n]},remove:function(n){delete this.files[n]},clear:function(){this.files={}}};function mm(n){try{let e=n.slice(n.indexOf(":")+1);return new URL(e).protocol==="blob:"}catch{return!1}}var dh=class{constructor(e,t,i){let s=this,r=!1,o=0,a=0,c,l=[];this.onStart=void 0,this.onLoad=e,this.onProgress=t,this.onError=i,this._abortController=null,this.itemStart=function(u){a++,r===!1&&s.onStart!==void 0&&s.onStart(u,o,a),r=!0},this.itemEnd=function(u){o++,s.onProgress!==void 0&&s.onProgress(u,o,a),o===a&&(r=!1,s.onLoad!==void 0&&s.onLoad())},this.itemError=function(u){s.onError!==void 0&&s.onError(u)},this.resolveURL=function(u){return u=u.normalize("NFC"),c?c(u):u},this.setURLModifier=function(u){return c=u,this},this.addHandler=function(u,d){return l.push(u,d),this},this.removeHandler=function(u){let d=l.indexOf(u);return d!==-1&&l.splice(d,2),this},this.getHandler=function(u){for(let d=0,f=l.length;d<f;d+=2){let p=l[d],x=l[d+1];if(p.global&&(p.lastIndex=0),p.test(u))return x}return null},this.abort=function(){return this.abortController.abort(),this._abortController=null,this}}get abortController(){return this._abortController||(this._abortController=new AbortController),this._abortController}},l0=new dh,Ms=class{constructor(e){this.manager=e!==void 0?e:l0,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}load(){}loadAsync(e,t){let i=this;return new Promise(function(s,r){i.load(e,s,t,r)})}parse(){}setCrossOrigin(e){return this.crossOrigin=e,this}setWithCredentials(e){return this.withCredentials=e,this}setPath(e){return this.path=e,this}setResourcePath(e){return this.resourcePath=e,this}setRequestHeader(e){return this.requestHeader=e,this}abort(){return this}};Ms.DEFAULT_MATERIAL_NAME="__DEFAULT";var Hs={},xd=class extends Error{constructor(e,t){super(e),this.response=t}},na=class extends Ms{constructor(e){super(e),this.mimeType="",this.responseType="",this._abortController=new AbortController}load(e,t,i,s){e===void 0&&(e=""),this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);let r=_s.get(`file:${e}`);if(r!==void 0){this.manager.itemStart(e),setTimeout(()=>{t&&t(r),this.manager.itemEnd(e)},0);return}if(Hs[e]!==void 0){Hs[e].push({onLoad:t,onProgress:i,onError:s});return}Hs[e]=[],Hs[e].push({onLoad:t,onProgress:i,onError:s});let o=new Request(e,{headers:new Headers(this.requestHeader),credentials:this.withCredentials?"include":"same-origin",signal:typeof AbortSignal.any=="function"?AbortSignal.any([this._abortController.signal,this.manager.abortController.signal]):this._abortController.signal}),a=this.mimeType,c=this.responseType;fetch(o).then(l=>{if(l.status===200||l.status===0){if(l.status===0&&nt("FileLoader: HTTP Status 0 received."),typeof ReadableStream>"u"||l.body===void 0||l.body.getReader===void 0)return l;let u=Hs[e],d=l.body.getReader(),f=l.headers.get("X-File-Size")||l.headers.get("Content-Length"),p=f?parseInt(f):0,x=p!==0,b=0,g=new ReadableStream({start(m){A();function A(){d.read().then(({done:U,value:T})=>{if(U)m.close();else{b+=T.byteLength;let I=new ProgressEvent("progress",{lengthComputable:x,loaded:b,total:p});for(let L=0,P=u.length;L<P;L++){let M=u[L];M.onProgress&&M.onProgress(I)}m.enqueue(T),A()}},U=>{m.error(U)})}}});return new Response(g)}else throw new xd(`fetch for "${l.url}" responded with ${l.status}: ${l.statusText}`,l)}).then(l=>{switch(c){case"arraybuffer":return l.arrayBuffer();case"blob":return l.blob();case"document":return l.text().then(u=>new DOMParser().parseFromString(u,a));case"json":return l.json();default:if(a==="")return l.text();{let d=/charset="?([^;"\s]*)"?/i.exec(a),f=d&&d[1]?d[1].toLowerCase():void 0,p=new TextDecoder(f);return l.arrayBuffer().then(x=>p.decode(x))}}}).then(l=>{_s.add(`file:${e}`,l);let u=Hs[e];delete Hs[e];for(let d=0,f=u.length;d<f;d++){let p=u[d];p.onLoad&&p.onLoad(l)}}).catch(l=>{let u=Hs[e];if(u===void 0)throw this.manager.itemError(e),l;delete Hs[e];for(let d=0,f=u.length;d<f;d++){let p=u[d];p.onError&&p.onError(l)}this.manager.itemError(e)}).finally(()=>{this.manager.itemEnd(e)}),this.manager.itemStart(e)}setResponseType(e){return this.responseType=e,this}setMimeType(e){return this.mimeType=e,this}abort(){return this._abortController.abort(),this._abortController=new AbortController,this}};var Bo=new WeakMap,fh=class extends Ms{constructor(e){super(e)}load(e,t,i,s){this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);let r=this,o=_s.get(`image:${e}`);if(o!==void 0){if(o.complete===!0)r.manager.itemStart(e),setTimeout(function(){t&&t(o),r.manager.itemEnd(e)},0);else{let d=Bo.get(o);d===void 0&&(d=[],Bo.set(o,d)),d.push({onLoad:t,onError:s})}return o}let a=qo("img");function c(){u(),t&&t(this);let d=Bo.get(this)||[];for(let f=0;f<d.length;f++){let p=d[f];p.onLoad&&p.onLoad(this)}Bo.delete(this),r.manager.itemEnd(e)}function l(d){u(),s&&s(d),_s.remove(`image:${e}`);let f=Bo.get(this)||[];for(let p=0;p<f.length;p++){let x=f[p];x.onError&&x.onError(d)}Bo.delete(this),r.manager.itemError(e),r.manager.itemEnd(e)}function u(){a.removeEventListener("load",c,!1),a.removeEventListener("error",l,!1)}return a.addEventListener("load",c,!1),a.addEventListener("error",l,!1),e.slice(0,5)!=="data:"&&this.crossOrigin!==void 0&&(a.crossOrigin=this.crossOrigin),_s.add(`image:${e}`,a),r.manager.itemStart(e),a.src=e,a}};var dl=class extends Ms{constructor(e){super(e)}load(e,t,i,s){let r=new In,o=new fh(this.manager);return o.setCrossOrigin(this.crossOrigin),o.setPath(this.path),o.load(e,function(a){r.image=a,r.needsUpdate=!0,t!==void 0&&t(r)},i,s),r}},Jr=class extends an{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ke(e),this.intensity=t}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){let t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,t}},fl=class extends Jr{constructor(e,t,i){super(e,i),this.isHemisphereLight=!0,this.type="HemisphereLight",this.position.copy(an.DEFAULT_UP),this.updateMatrix(),this.groundColor=new ke(t)}copy(e,t){return super.copy(e,t),this.groundColor.copy(e.groundColor),this}toJSON(e){let t=super.toJSON(e);return t.object.groundColor=this.groundColor.getHex(),t}},cd=new rt,gm=new y,_m=new y,ia=class{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.biasNode=null,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Pe(512,512),this.mapType=di,this.map=null,this.mapPass=null,this.matrix=new rt,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new ea,this._frameExtents=new Pe(1,1),this._viewportCount=1,this._viewports=[new $t(0,0,1,1)]}getViewportCount(){return this._viewportCount}getCamera(){return this.camera}getFrustum(){return this._frustum}updateMatrices(e){let t=this.camera;gm.setFromMatrixPosition(e.matrixWorld),t.position.copy(gm),_m.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(_m),t.updateMatrixWorld(),this._updateMatrix(t,this.matrix,this._frustum)}_updateMatrix(e,t,i,s){cd.multiplyMatrices(e.projectionMatrix,e.matrixWorldInverse),i.setFromProjectionMatrix(cd,e.coordinateSystem,e.reversedDepth);let r=this._frameExtents,o=s?s.z/r.x:1,a=s?s.w/r.y:1,c=s?s.x/r.x:0,l=s?s.y/r.y:0;e.coordinateSystem===Xo||e.reversedDepth?t.set(.5*o,0,0,.5*o+c,0,.5*a,0,.5*a+l,0,0,1,0,0,0,0,1):t.set(.5*o,0,0,.5*o+c,0,.5*a,0,.5*a+l,0,0,.5,.5,0,0,0,1),t.multiply(cd)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.autoUpdate=e.autoUpdate,this.needsUpdate=e.needsUpdate,this.normalBias=e.normalBias,this.blurSamples=e.blurSamples,this.mapSize.copy(e.mapSize),this.biasNode=e.biasNode,this}clone(){return new this.constructor().copy(this)}toJSON(){let e={};return e.intensity=this.intensity,e.bias=this.bias,e.normalBias=this.normalBias,e.radius=this.radius,e.blurSamples=this.blurSamples,e.mapSize=this.mapSize.toArray(),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}},Dc=new y,Nc=new rn,ms=new y,pl=class extends an{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new rt,this.projectionMatrix=new rt,this.projectionMatrixInverse=new rt,this.coordinateSystem=ji,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorld.decompose(Dc,Nc,ms),ms.x===1&&ms.y===1&&ms.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Dc,Nc,ms.set(1,1,1)).invert()}updateWorldMatrix(e,t,i=!1){super.updateWorldMatrix(e,t,i),this.matrixWorld.decompose(Dc,Nc,ms),ms.x===1&&ms.y===1&&ms.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Dc,Nc,ms.set(1,1,1)).invert()}clone(){return new this.constructor().copy(this)}},ar=new y,xm=new Pe,vm=new Pe,An=class extends pl{constructor(e=50,t=1,i=.1,s=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=s,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){let t=.5*this.getFilmHeight()/e;this.fov=Gr*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){let e=Math.tan(Vo*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return Gr*2*Math.atan(Math.tan(Vo*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){ar.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(ar.x,ar.y).multiplyScalar(-e/ar.z),ar.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(ar.x,ar.y).multiplyScalar(-e/ar.z)}getViewSize(e,t){return this.getViewBounds(e,xm,vm),t.subVectors(vm,xm)}setViewOffset(e,t,i,s,r,o){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=s,this.view.width=r,this.view.height=o,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=this.near,t=e*Math.tan(Vo*.5*this.fov)/this.zoom,i=2*t,s=this.aspect*i,r=-.5*s,o=this.view;if(this.view!==null&&this.view.enabled){let c=o.fullWidth,l=o.fullHeight;r+=o.offsetX*s/c,t-=o.offsetY*i/l,s*=o.width/c,i*=o.height/l}let a=this.filmOffset;a!==0&&(r+=e*a/this.getFilmWidth()),this.projectionMatrix.makePerspective(r,r+s,t,t-i,e,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}},vd=class extends ia{constructor(){super(new An(50,1,.5,500)),this.isSpotLightShadow=!0,this.focus=1,this.aspect=1}updateMatrices(e){let t=this.camera,i=Gr*2*e.angle*this.focus,s=this.mapSize.width/this.mapSize.height*this.aspect,r=e.distance||t.far;(i!==t.fov||s!==t.aspect||r!==t.far)&&(t.fov=i,t.aspect=s,t.far=r,t.updateProjectionMatrix()),super.updateMatrices(e)}copy(e){return super.copy(e),this.focus=e.focus,this.aspect=e.aspect,this}toJSON(){let e=super.toJSON();return e.focus=this.focus,e.aspect=this.aspect,e}},ml=class extends Jr{constructor(e,t,i=0,s=Math.PI/3,r=0,o=2){super(e,t),this.isSpotLight=!0,this.type="SpotLight",this.position.copy(an.DEFAULT_UP),this.updateMatrix(),this.target=new an,this.distance=i,this.angle=s,this.penumbra=r,this.decay=o,this.map=null,this.shadow=new vd}get power(){return this.intensity*Math.PI}set power(e){this.intensity=e/Math.PI}dispose(){super.dispose(),this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.angle=e.angle,this.penumbra=e.penumbra,this.decay=e.decay,this.target=e.target.clone(),this.map=e.map,this.shadow=e.shadow.clone(),this}toJSON(e){let t=super.toJSON(e);return t.object.distance=this.distance,t.object.angle=this.angle,t.object.decay=this.decay,t.object.penumbra=this.penumbra,t.object.target=this.target.uuid,this.map&&this.map.isTexture&&(t.object.map=this.map.toJSON(e).uuid),t.object.shadow=this.shadow.toJSON(),t}},yd=class extends ia{constructor(){super(new An(90,1,.5,500)),this.isPointLightShadow=!0}},Di=class extends Jr{constructor(e,t,i=0,s=2){super(e,t),this.isPointLight=!0,this.type="PointLight",this.distance=i,this.decay=s,this.shadow=new yd}get power(){return this.intensity*4*Math.PI}set power(e){this.intensity=e/(4*Math.PI)}dispose(){super.dispose(),this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.decay=e.decay,this.shadow=e.shadow.clone(),this}toJSON(e){let t=super.toJSON(e);return t.object.distance=this.distance,t.object.decay=this.decay,t.object.shadow=this.shadow.toJSON(),t}},mr=class extends pl{constructor(e=-1,t=1,i=1,s=-1,r=.1,o=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=s,this.near=r,this.far=o,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,s,r,o){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=s,this.view.width=r,this.view.height=o,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,s=(this.top+this.bottom)/2,r=i-e,o=i+e,a=s+t,c=s-t;if(this.view!==null&&this.view.enabled){let l=(this.right-this.left)/this.view.fullWidth/this.zoom,u=(this.top-this.bottom)/this.view.fullHeight/this.zoom;r+=l*this.view.offsetX,o=r+l*this.view.width,a-=u*this.view.offsetY,c=a-u*this.view.height}this.projectionMatrix.makeOrthographic(r,o,a,c,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}},Md=class extends ia{constructor(){super(new mr(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}},Qr=class extends Jr{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(an.DEFAULT_UP),this.updateMatrix(),this.target=new an,this.shadow=new Md}dispose(){super.dispose(),this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}toJSON(e){let t=super.toJSON(e);return t.object.shadow=this.shadow.toJSON(),t.object.target=this.target.uuid,t}};var Ys=class{static extractUrlBase(e){let t=e.lastIndexOf("/");return t===-1?"./":e.slice(0,t+1)}static resolveURL(e,t){return typeof e!="string"||e===""?"":(/^https?:\/\//i.test(t)&&/^\//.test(e)&&(t=t.replace(/(^https?:\/\/[^\/]+).*/i,"$1")),/^(https?:)?\/\//i.test(e)||/^data:.*,.*$/i.test(e)||/^blob:.*$/i.test(e)?e:t+e)}};var hd=new WeakMap,gl=class extends Ms{constructor(e){super(e),this.isImageBitmapLoader=!0,typeof createImageBitmap>"u"&&nt("ImageBitmapLoader: createImageBitmap() not supported."),typeof fetch>"u"&&nt("ImageBitmapLoader: fetch() not supported."),this.options={premultiplyAlpha:"none"},this._abortController=new AbortController}setOptions(e){return this.options=e,this}load(e,t,i,s){e===void 0&&(e=""),this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);let r=this,o=_s.get(`image-bitmap:${e}`);if(o!==void 0){if(r.manager.itemStart(e),o.then){o.then(l=>{hd.has(o)===!0?(s&&s(hd.get(o)),r.manager.itemError(e),r.manager.itemEnd(e)):(t&&t(l),r.manager.itemEnd(e))});return}setTimeout(function(){t&&t(o),r.manager.itemEnd(e)},0);return}let a={};a.credentials=this.crossOrigin==="anonymous"?"same-origin":"include",a.headers=this.requestHeader,a.signal=typeof AbortSignal.any=="function"?AbortSignal.any([this._abortController.signal,this.manager.abortController.signal]):this._abortController.signal;let c=fetch(e,a).then(function(l){return l.blob()}).then(function(l){return createImageBitmap(l,Object.assign({},r.options,{colorSpaceConversion:"none"}))}).then(function(l){return _s.add(`image-bitmap:${e}`,l),t&&t(l),r.manager.itemEnd(e),l}).catch(function(l){s&&s(l),hd.set(c,l),_s.remove(`image-bitmap:${e}`),r.manager.itemError(e),r.manager.itemEnd(e)});_s.add(`image-bitmap:${e}`,c),r.manager.itemStart(e)}abort(){return this._abortController.abort(),this._abortController=new AbortController,this}};var Ho=-90,ko=1,ph=class extends an{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;let s=new An(Ho,ko,e,t);s.layers=this.layers,this.add(s);let r=new An(Ho,ko,e,t);r.layers=this.layers,this.add(r);let o=new An(Ho,ko,e,t);o.layers=this.layers,this.add(o);let a=new An(Ho,ko,e,t);a.layers=this.layers,this.add(a);let c=new An(Ho,ko,e,t);c.layers=this.layers,this.add(c);let l=new An(Ho,ko,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){let e=this.coordinateSystem,t=this.children.concat(),[i,s,r,o,a,c]=t;for(let l of t)this.remove(l);if(e===ji)i.up.set(0,1,0),i.lookAt(1,0,0),s.up.set(0,1,0),s.lookAt(-1,0,0),r.up.set(0,0,-1),r.lookAt(0,1,0),o.up.set(0,0,1),o.lookAt(0,-1,0),a.up.set(0,1,0),a.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===Xo)i.up.set(0,-1,0),i.lookAt(-1,0,0),s.up.set(0,-1,0),s.lookAt(1,0,0),r.up.set(0,0,1),r.lookAt(0,1,0),o.up.set(0,0,-1),o.lookAt(0,-1,0),a.up.set(0,-1,0),a.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(let l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();let{renderTarget:i,activeMipmapLevel:s}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());let[r,o,a,c,l,u]=this.children,d=e.getRenderTarget(),f=e.getActiveCubeFace(),p=e.getActiveMipmapLevel(),x=e.xr.enabled;e.xr.enabled=!1;let b=i.texture.generateMipmaps;i.texture.generateMipmaps=!1;let g=!1;e.isWebGLRenderer===!0?g=e.state.buffers.depth.getReversed():g=e.reversedDepthBuffer,e.setRenderTarget(i,0,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,r),e.setRenderTarget(i,1,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,o),e.setRenderTarget(i,2,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,a),e.setRenderTarget(i,3,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,c),e.setRenderTarget(i,4,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,l),i.texture.generateMipmaps=b,e.setRenderTarget(i,5,s),g&&e.autoClear===!1&&e.clearDepth(),e.render(t,u),e.setRenderTarget(d,f,p),e.xr.enabled=x,i.texture.needsPMREMUpdate=!0}},mh=class extends An{constructor(e=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=e}};var Kd="\\[\\]\\.:\\/",J_=new RegExp("["+Kd+"]","g"),jd="[^"+Kd+"]",Q_="[^"+Kd.replace("\\.","")+"]",ex=/((?:WC+[\/:])*)/.source.replace("WC",jd),tx=/(WCOD+)?/.source.replace("WCOD",Q_),nx=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",jd),ix=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",jd),sx=new RegExp("^"+ex+tx+nx+ix+"$"),rx=["material","materials","bones","map"],Ed=class{constructor(e,t,i){let s=i||en.parseTrackName(t);this._targetGroup=e,this._bindings=e.subscribe_(t,s)}getValue(e,t){this.bind();let i=this._targetGroup.nCachedObjects_,s=this._bindings[i];s!==void 0&&s.getValue(e,t)}setValue(e,t){let i=this._bindings;for(let s=this._targetGroup.nCachedObjects_,r=i.length;s!==r;++s)i[s].setValue(e,t)}bind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,i=e.length;t!==i;++t)e[t].bind()}unbind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,i=e.length;t!==i;++t)e[t].unbind()}},en=class n{constructor(e,t,i){this.path=t,this.parsedPath=i||n.parseTrackName(t),this.node=n.findNode(e,this.parsedPath.nodeName),this.rootNode=e,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(e,t,i){return e&&e.isAnimationObjectGroup?new n.Composite(e,t,i):new n(e,t,i)}static sanitizeNodeName(e){return e.replace(/\s/g,"_").replace(J_,"")}static parseTrackName(e){let t=sx.exec(e);if(t===null)throw new Error("THREE.PropertyBinding: Cannot parse trackName: "+e);let i={nodeName:t[2],objectName:t[3],objectIndex:t[4],propertyName:t[5],propertyIndex:t[6]},s=i.nodeName&&i.nodeName.lastIndexOf(".");if(s!==void 0&&s!==-1){let r=i.nodeName.substring(s+1);rx.indexOf(r)!==-1&&(i.nodeName=i.nodeName.substring(0,s),i.objectName=r)}if(i.propertyName===null||i.propertyName.length===0)throw new Error("THREE.PropertyBinding: can not parse propertyName from trackName: "+e);return i}static findNode(e,t){if(t===void 0||t===""||t==="."||t===-1||t===e.name||t===e.uuid)return e;if(e.skeleton){let i=e.skeleton.getBoneByName(t);if(i!==void 0)return i}if(e.children){let i=function(r){for(let o=0;o<r.length;o++){let a=r[o];if(a.name===t||a.uuid===t)return a;let c=i(a.children);if(c)return c}return null},s=i(e.children);if(s)return s}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(e,t){e[t]=this.targetObject[this.propertyName]}_getValue_array(e,t){let i=this.resolvedProperty;for(let s=0,r=i.length;s!==r;++s)e[t++]=i[s]}_getValue_arrayElement(e,t){e[t]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(e,t){this.resolvedProperty.toArray(e,t)}_setValue_direct(e,t){this.targetObject[this.propertyName]=e[t]}_setValue_direct_setNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(e,t){let i=this.resolvedProperty;for(let s=0,r=i.length;s!==r;++s)i[s]=e[t++]}_setValue_array_setNeedsUpdate(e,t){let i=this.resolvedProperty;for(let s=0,r=i.length;s!==r;++s)i[s]=e[t++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(e,t){let i=this.resolvedProperty;for(let s=0,r=i.length;s!==r;++s)i[s]=e[t++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(e,t){this.resolvedProperty[this.propertyIndex]=e[t]}_setValue_arrayElement_setNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(e,t){this.resolvedProperty.fromArray(e,t)}_setValue_fromArray_setNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(e,t){this.bind(),this.getValue(e,t)}_setValue_unbound(e,t){this.bind(),this.setValue(e,t)}bind(){let e=this.node,t=this.parsedPath,i=t.objectName,s=t.propertyName,r=t.propertyIndex;if(e||(e=n.findNode(this.rootNode,t.nodeName),this.node=e),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!e){nt("PropertyBinding: No target node found for track: "+this.path+".");return}if(i){let l=t.objectIndex;switch(i){case"materials":if(!e.material){ht("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.materials){ht("PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}e=e.material.materials;break;case"bones":if(!e.skeleton){ht("PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}e=e.skeleton.bones;for(let u=0;u<e.length;u++)if(e[u].name===l){l=u;break}break;case"map":if("map"in e){e=e.map;break}if(!e.material){ht("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.map){ht("PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}e=e.material.map;break;default:if(e[i]===void 0){ht("PropertyBinding: Can not bind to objectName of node undefined.",this);return}e=e[i]}if(l!==void 0){if(e[l]===void 0){ht("PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,e);return}e=e[l]}}let o=e[s];if(o===void 0){let l=t.nodeName;ht("PropertyBinding: Trying to update property for track: "+l+"."+s+" but it wasn't found.",e);return}let a=this.Versioning.None;this.targetObject=e,e.isMaterial===!0?a=this.Versioning.NeedsUpdate:e.isObject3D===!0&&(a=this.Versioning.MatrixWorldNeedsUpdate);let c=this.BindingType.Direct;if(r!==void 0){if(s==="morphTargetInfluences"){if(!e.geometry){ht("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!e.geometry.morphAttributes){ht("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}e.morphTargetDictionary[r]!==void 0&&(r=e.morphTargetDictionary[r])}c=this.BindingType.ArrayElement,this.resolvedProperty=o,this.propertyIndex=r}else o.fromArray!==void 0&&o.toArray!==void 0?(c=this.BindingType.HasFromToArray,this.resolvedProperty=o):Array.isArray(o)?(c=this.BindingType.EntireArray,this.resolvedProperty=o):this.propertyName=s;this.getValue=this.GetterByBindingType[c],this.setValue=this.SetterByBindingTypeAndVersioning[c][a]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};en.Composite=Ed;en.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};en.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};en.prototype.GetterByBindingType=[en.prototype._getValue_direct,en.prototype._getValue_array,en.prototype._getValue_arrayElement,en.prototype._getValue_toArray];en.prototype.SetterByBindingTypeAndVersioning=[[en.prototype._setValue_direct,en.prototype._setValue_direct_setNeedsUpdate,en.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[en.prototype._setValue_array,en.prototype._setValue_array_setNeedsUpdate,en.prototype._setValue_array_setMatrixWorldNeedsUpdate],[en.prototype._setValue_arrayElement,en.prototype._setValue_arrayElement_setNeedsUpdate,en.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[en.prototype._setValue_fromArray,en.prototype._setValue_fromArray_setNeedsUpdate,en.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var xb=new Float32Array(1);var ym=new rt,_l=class{constructor(e,t,i=0,s=1/0){this.ray=new vs(e,t),this.near=i,this.far=s,this.camera=null,this.layers=new Zo,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,t.projectionMatrix.elements[14]).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):ht("Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return ym.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(ym),this}intersectObject(e,t=!0,i=[]){return bd(e,this,i,t),i.sort(Mm),i}intersectObjects(e,t=!0,i=[]){for(let s=0,r=e.length;s<r;s++)bd(e[s],this,i,t);return i.sort(Mm),i}};function Mm(n,e){return n.distance-e.distance}function bd(n,e,t,i){let s=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(s=!1),s===!0&&i===!0){let r=n.children;for(let o=0,a=r.length;o<a;o++)bd(r[o],e,t,!0)}}var xl=class{constructor(e=!0){this.autoStart=e,this.startTime=0,this.oldTime=0,this.elapsedTime=0,this.running=!1,nt("Clock: This module has been deprecated. Please use THREE.Timer instead.")}start(){this.startTime=performance.now(),this.oldTime=this.startTime,this.elapsedTime=0,this.running=!0}stop(){this.getElapsedTime(),this.running=!1,this.autoStart=!1}getElapsedTime(){return this.getDelta(),this.elapsedTime}getDelta(){let e=0;if(this.autoStart&&!this.running)return this.start(),0;if(this.running){let t=performance.now();e=(t-this.oldTime)/1e3,this.oldTime=t,this.elapsedTime+=e}return e}},sa=class{constructor(e=1,t=0,i=0){this.radius=e,this.phi=t,this.theta=i}set(e,t,i){return this.radius=e,this.phi=t,this.theta=i,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=St(this.phi,1e-6,Math.PI-1e-6),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,t,i){return this.radius=Math.sqrt(e*e+t*t+i*i),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,i),this.phi=Math.acos(St(t/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}};var Td=class n{static{n.prototype.isMatrix2=!0}constructor(e,t,i,s){this.elements=[1,0,0,1],e!==void 0&&this.set(e,t,i,s)}identity(){return this.set(1,0,0,1),this}fromArray(e,t=0){for(let i=0;i<4;i++)this.elements[i]=e[i+t];return this}set(e,t,i,s){let r=this.elements;return r[0]=e,r[2]=t,r[1]=i,r[3]=s,this}};var vl=class extends Qi{constructor(e,t=null){super(),this.object=e,this.domElement=t,this.enabled=!0,this.state=-1,this.keys={},this.mouseButtons={LEFT:null,MIDDLE:null,RIGHT:null},this.touches={ONE:null,TWO:null}}connect(e){this.domElement!==null&&this.disconnect(),this.domElement=e}disconnect(){}dispose(){}update(){}};function Jd(n,e,t,i){let s=ox(i);switch(t){case zd:return n*e;case bh:return n*e/s.components*s.byteLength;case Th:return n*e/s.components*s.byteLength;case xr:return n*e*2/s.components*s.byteLength;case Sh:return n*e*2/s.components*s.byteLength;case Gd:return n*e*3/s.components*s.byteLength;case Si:return n*e*4/s.components*s.byteLength;case wh:return n*e*4/s.components*s.byteLength;case bl:case Tl:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Sl:case wl:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Rh:case Ih:return Math.max(n,16)*Math.max(e,8)/4;case Ah:case Ch:return Math.max(n,8)*Math.max(e,8)/2;case Ph:case Lh:case Nh:case Uh:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Dh:case Al:case Fh:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Oh:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Bh:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case Hh:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case kh:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case Vh:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case zh:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case Gh:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case Wh:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case Xh:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case qh:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case Yh:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case $h:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case Zh:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case Kh:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case jh:case Jh:case Qh:return Math.ceil(n/4)*Math.ceil(e/4)*16;case eu:case tu:return Math.ceil(n/4)*Math.ceil(e/4)*8;case Rl:case nu:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function ox(n){switch(n){case di:case Bd:return{byteLength:1,components:1};case la:case Hd:case rs:return{byteLength:2,components:1};case Mh:case Eh:return{byteLength:2,components:4};case ss:case yh:case Ti:return{byteLength:4,components:1};case kd:case Vd:return{byteLength:4,components:3}}throw new Error(`THREE.TextureUtils: Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:"186"}}));typeof window<"u"&&(window.__THREE__?nt("WARNING: Multiple instances of Three.js being imported."):window.__THREE__="186");function I0(){let n=null,e=!1,t=null,i=null;function s(r,o){i=n.requestAnimationFrame(s),t(r,o)}return{start:function(){e!==!0&&t!==null&&n!==null&&(i=n.requestAnimationFrame(s),e=!0)},stop:function(){n!==null&&n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(r){t=r},setContext:function(r){n=r}}}function lx(n){let e=new WeakMap;function t(a,c){let l=a.array,u=a.usage,d=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,u),a.onUploadCallback();let p;if(l instanceof Float32Array)p=n.FLOAT;else if(typeof Float16Array<"u"&&l instanceof Float16Array)p=n.HALF_FLOAT;else if(l instanceof Uint16Array)a.isFloat16BufferAttribute?p=n.HALF_FLOAT:p=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)p=n.SHORT;else if(l instanceof Uint32Array)p=n.UNSIGNED_INT;else if(l instanceof Int32Array)p=n.INT;else if(l instanceof Int8Array)p=n.BYTE;else if(l instanceof Uint8Array)p=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)p=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:p,bytesPerElement:l.BYTES_PER_ELEMENT,version:a.version,size:d}}function i(a,c,l){let u=c.array,d=c.updateRanges;if(n.bindBuffer(l,a),d.length===0)n.bufferSubData(l,0,u);else{d.sort((p,x)=>p.start-x.start);let f=0;for(let p=1;p<d.length;p++){let x=d[f],b=d[p];b.start<=x.start+x.count+1?x.count=Math.max(x.count,b.start+b.count-x.start):(++f,d[f]=b)}d.length=f+1;for(let p=0,x=d.length;p<x;p++){let b=d[p];n.bufferSubData(l,b.start*u.BYTES_PER_ELEMENT,u,b.start,b.count)}c.clearUpdateRanges()}c.onUploadCallback()}function s(a){return a.isInterleavedBufferAttribute&&(a=a.data),e.get(a)}function r(a){a.isInterleavedBufferAttribute&&(a=a.data);let c=e.get(a);c&&(n.deleteBuffer(c.buffer),e.delete(a))}function o(a,c){if(a.isInterleavedBufferAttribute&&(a=a.data),a.isGLBufferAttribute){let u=e.get(a);(!u||u.version<a.version)&&e.set(a,{buffer:a.buffer,type:a.type,bytesPerElement:a.elementSize,version:a.version});return}let l=e.get(a);if(l===void 0)e.set(a,t(a,c));else if(l.version<a.version){if(l.size!==a.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,a,c),l.version=a.version}}return{get:s,remove:r,update:o}}var cx=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,hx=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,ux=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,dx=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,fx=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,px=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,mx=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,gx=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,_x=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec4 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 );
	}
#endif`,xx=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,vx=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,yx=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Mx=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,Ex=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,bx=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,Tx=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,Sx=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,wx=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,Ax=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Rx=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#endif`,Cx=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#endif`,Ix=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec4 vColor;
#endif`,Px=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec4( 1.0 );
#endif
#ifdef USE_COLOR_ALPHA
	vColor *= color;
#elif defined( USE_COLOR )
	vColor.rgb *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.rgb *= instanceColor.rgb;
#endif
#ifdef USE_BATCHING_COLOR
	vColor *= getBatchingColor( getIndirectIndex( gl_DrawID ) );
#endif`,Lx=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
#define inverseTransformDirection transformDirectionByInverseViewMatrix
vec3 transformNormalByInverseViewMatrix( in vec3 normal, in mat4 viewMatrix ) {
	return normalize( ( vec4( normal, 0.0 ) * viewMatrix ).xyz );
}
vec3 transformDirectionByInverseViewMatrix( in vec3 dir, in mat4 viewMatrix ) {
	return normalize( ( vec4( dir, 0.0 ) * viewMatrix ).xyz );
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,Dx=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,Nx=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
#endif`,Ux=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Fx=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Ox=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,Bx=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Hx="gl_FragColor = linearToOutputTexel( gl_FragColor );",kx=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Vx=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * reflectVec );
		#ifdef ENVMAP_BLENDING_MULTIPLY
			outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_MIX )
			outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_ADD )
			outgoingLight += envColor.xyz * specularStrength * reflectivity;
		#endif
	#endif
#endif`,zx=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
#endif`,Gx=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,Wx=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Xx=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = transformNormalByInverseViewMatrix( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,qx=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Yx=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,$x=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Zx=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Kx=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,jx=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Jx=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Qx=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,ev=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_SUN_LIGHTS > 0
	struct SunLight {
		vec3 direction;
		vec3 color;
	};
	uniform SunLight sunLights[ NUM_SUN_LIGHTS ];
	void getSunLightInfo( const in SunLight sunLight, out IncidentLight light ) {
		light.color = sunLight.color;
		light.direction = sunLight.direction;
		light.visible = true;
	}
#endif
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif
#include <lightprobes_pars_fragment>`,tv=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, pow4( roughness ) ) );
			reflectVec = transformDirectionByInverseViewMatrix( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_RETROREFLECTION
		vec3 getIBLRetroRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 retroVec = normalize( mix( viewDir, normal, pow4( roughness ) ) );
				retroVec = transformDirectionByInverseViewMatrix( retroVec, viewMatrix );
				vec4 envMapColor = textureCubeUV( envMap, envMapRotation * retroVec, roughness );
				return envMapColor.rgb * envMapIntensity;
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
		#ifdef USE_RETROREFLECTION
			vec3 getIBLAnisotropyRetroRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
				#ifdef ENVMAP_TYPE_CUBE_UV
					vec3 bentNormal = cross( bitangent, viewDir );
					bentNormal = normalize( cross( bentNormal, bitangent ) );
					bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
					return getIBLRetroRadiance( viewDir, bentNormal, roughness );
				#else
					return vec3( 0.0 );
				#endif
			}
		#endif
	#endif
#endif`,nv=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,iv=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,sv=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,rv=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,ov=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.diffuseContribution = diffuseColor.rgb * ( 1.0 - metalnessFactor );
material.metalness = metalnessFactor;
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor;
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = vec3( 0.04 );
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_RETROREFLECTION
	material.retroreflectivity = retroreflectivity;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.0001, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,av=`uniform sampler2D dfgLUT;
struct PhysicalMaterial {
	vec3 diffuseColor;
	vec3 diffuseContribution;
	vec3 specularColor;
	vec3 specularColorBlended;
	float roughness;
	float metalness;
	float specularF90;
	float dispersion;
	vec2 dfg;
	vec3 multiScatteringCompensation;
	#ifdef USE_RETROREFLECTION
		float retroreflectivity;
	#endif
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0Dielectric;
		vec3 iridescenceF0Metallic;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		return 0.5 / max( gv + gl, EPSILON );
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColorBlended;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transpose( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float rInv = 1.0 / ( roughness + 0.1 );
	float a = -1.9362 + 1.0678 * roughness + 0.4573 * r2 - 0.8469 * rInv;
	float b = -0.6014 + 0.5538 * roughness - 0.4670 * r2 - 0.1255 * rInv;
	float DG = exp( a * dotNV + b );
	return saturate( DG );
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec2 fab, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec2 fab, const in vec3 specularColor, const in float specularF90, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColorBlended * t2.x + ( material.specularF90 - material.specularColorBlended ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseContribution * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
		#ifdef USE_CLEARCOAT
			vec3 Ncc = geometryClearcoatNormal;
			vec2 uvClearcoat = LTC_Uv( Ncc, viewDir, material.clearcoatRoughness );
			vec4 t1Clearcoat = texture2D( ltc_1, uvClearcoat );
			vec4 t2Clearcoat = texture2D( ltc_2, uvClearcoat );
			mat3 mInvClearcoat = mat3(
				vec3( t1Clearcoat.x, 0, t1Clearcoat.y ),
				vec3(             0, 1,             0 ),
				vec3( t1Clearcoat.z, 0, t1Clearcoat.w )
			);
			vec3 fresnelClearcoat = material.clearcoatF0 * t2Clearcoat.x + ( material.clearcoatF90 - material.clearcoatF0 ) * t2Clearcoat.y;
			clearcoatSpecularDirect += lightColor * fresnelClearcoat * LTC_Evaluate( Ncc, viewDir, position, mInvClearcoat, rectCoords );
		#endif
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
 
 		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
 
 		float sheenAlbedoV = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
 		float sheenAlbedoL = IBLSheenBRDF( geometryNormal, directLight.direction, material.sheenRoughness );
 
 		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * max( sheenAlbedoV, sheenAlbedoL );
 
 		irradiance *= sheenEnergyComp;
 
 	#endif
	vec3 specularBRDF = BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	#ifdef USE_RETROREFLECTION
		vec3 retroViewDir = reflect( - geometryViewDir, geometryNormal );
		vec3 retroSpecularBRDF = BRDF_GGX( directLight.direction, retroViewDir, geometryNormal, material );
		specularBRDF = mix( specularBRDF, retroSpecularBRDF, saturate( material.retroreflectivity ) );
	#endif
	reflectedLight.directSpecular += irradiance * specularBRDF * material.multiScatteringCompensation;
	vec3 halfDir = normalize( directLight.direction + geometryViewDir );
	float dotVH = saturate( dot( geometryViewDir, halfDir ) );
	vec3 F = F_Schlick( material.specularColor, material.specularF90, dotVH );
	#ifdef USE_RETROREFLECTION
		vec3 retroHalfDir = normalize( directLight.direction + retroViewDir );
		float dotRetroVH = saturate( dot( retroViewDir, retroHalfDir ) );
		vec3 retroF = F_Schlick( material.specularColor, material.specularF90, dotRetroVH );
		F = mix( F, retroF, saturate( material.retroreflectivity ) );
	#endif
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution ) * ( 1.0 - F );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( material.dfg, material.specularColor, material.specularF90, material.iridescence, material.iridescenceF0Dielectric, singleScattering, multiScattering );
	#else
		computeMultiscattering( material.dfg, material.specularColor, material.specularF90, singleScattering, multiScattering );
	#endif
	vec3 diffuse = irradiance * BRDF_Lambert( material.diffuseContribution ) * ( 1.0 - singleScattering - multiScattering );
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		sheenSpecularIndirect += irradiance * material.sheenColor * sheenAlbedo * RECIPROCAL_PI;
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		diffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectDiffuse += diffuse;
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness ) * RECIPROCAL_PI;
 	#endif
	vec3 singleScatteringDielectric = vec3( 0.0 );
	vec3 multiScatteringDielectric = vec3( 0.0 );
	vec3 singleScatteringMetallic = vec3( 0.0 );
	vec3 multiScatteringMetallic = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( material.dfg, material.specularColor, material.specularF90, material.iridescence, material.iridescenceF0Dielectric, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscatteringIridescence( material.dfg, material.diffuseColor, material.specularF90, material.iridescence, material.iridescenceF0Metallic, singleScatteringMetallic, multiScatteringMetallic );
	#else
		computeMultiscattering( material.dfg, material.specularColor, material.specularF90, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscattering( material.dfg, material.diffuseColor, material.specularF90, singleScatteringMetallic, multiScatteringMetallic );
	#endif
	vec3 singleScattering = mix( singleScatteringDielectric, singleScatteringMetallic, material.metalness );
	vec3 multiScattering = mix( multiScatteringDielectric, multiScatteringMetallic, material.metalness );
	vec3 totalScatteringDielectric = singleScatteringDielectric + multiScatteringDielectric;
	vec3 diffuse = material.diffuseContribution * ( 1.0 - totalScatteringDielectric );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	vec3 indirectSpecular = radiance * singleScattering;
	indirectSpecular += multiScattering * cosineWeightedIrradiance;
	vec3 indirectDiffuse = diffuse * cosineWeightedIrradiance;
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		indirectSpecular *= sheenEnergyComp;
		indirectDiffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectSpecular += indirectSpecular;
	reflectedLight.indirectDiffuse += indirectDiffuse;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,lv=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		vec3 iridescenceFresnelDielectric = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		vec3 iridescenceFresnelMetallic = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.diffuseColor );
		material.iridescenceFresnel = mix( iridescenceFresnelDielectric, iridescenceFresnelMetallic, material.metalness );
		material.iridescenceF0Dielectric = Schlick_to_F0( iridescenceFresnelDielectric, 1.0, dotNVi );
		material.iridescenceF0Metallic = Schlick_to_F0( iridescenceFresnelMetallic, 1.0, dotNVi );
	}
#endif
#ifdef STANDARD
	float dotNVms = saturate( dot( geometryNormal, geometryViewDir ) );
	material.dfg = texture2D( dfgLUT, vec2( material.roughness, dotNVms ) ).rg;
	#if ( NUM_SUN_LIGHTS > 0 || NUM_DIR_LIGHTS > 0 || NUM_POINT_LIGHTS > 0 || NUM_SPOT_LIGHTS > 0 )
		float EssMs = material.dfg.x + material.dfg.y;
		material.multiScatteringCompensation = 1.0 + material.specularColorBlended * ( 1.0 / EssMs - 1.0 );
	#endif
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS ) && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SUN_LIGHTS > 0 ) && defined( RE_Direct )
	SunLight sunLight;
	#if defined( USE_SHADOWMAP ) && NUM_SUN_LIGHT_SHADOWS > 0
	SunLightShadow sunLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SUN_LIGHTS; i ++ ) {
		sunLight = sunLights[ i ];
		getSunLightInfo( sunLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SUN_LIGHT_SHADOWS )
		sunLightShadow = sunLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getSunShadow( sunShadowMap[ i ], sunLightShadow, UNROLLED_LOOP_INDEX ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
	#ifdef USE_LIGHT_PROBES_GRID
		vec3 probeWorldPos = ( ( vec4( geometryPosition, 1.0 ) - viewMatrix[ 3 ] ) * viewMatrix ).xyz;
		vec3 probeWorldNormal = transformNormalByInverseViewMatrix( geometryNormal, viewMatrix );
		irradiance += getLightProbeGridIrradiance( probeWorldPos, probeWorldNormal );
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,cv=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( ENVMAP_TYPE_CUBE_UV )
		#if defined( STANDARD ) || defined( LAMBERT ) || defined( PHONG )
			iblIrradiance += getIBLIrradiance( geometryNormal );
		#endif
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		vec3 iblRadiance = getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		vec3 iblRadiance = getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_RETROREFLECTION
		#ifdef USE_ANISOTROPY
			vec3 retroIBLRadiance = getIBLAnisotropyRetroRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
		#else
			vec3 retroIBLRadiance = getIBLRetroRadiance( geometryViewDir, geometryNormal, material.roughness );
		#endif
		iblRadiance = mix( iblRadiance, retroIBLRadiance, saturate( material.retroreflectivity ) );
	#endif
	radiance += iblRadiance;
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,hv=`#if defined( RE_IndirectDiffuse )
	#if defined( LAMBERT ) || defined( PHONG )
		irradiance += iblIrradiance;
	#endif
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,uv=`#ifdef USE_LIGHT_PROBES_GRID
uniform highp sampler3D probesSH;
uniform vec3 probesMin;
uniform vec3 probesMax;
uniform vec3 probesResolution;
vec3 getLightProbeGridIrradiance( vec3 worldPos, vec3 worldNormal ) {
	vec3 res = probesResolution;
	vec3 gridRange = probesMax - probesMin;
	vec3 resMinusOne = res - 1.0;
	vec3 probeSpacing = gridRange / resMinusOne;
	vec3 samplePos = worldPos + worldNormal * probeSpacing * 0.5;
	vec3 uvw = clamp( ( samplePos - probesMin ) / gridRange, 0.0, 1.0 );
	uvw = uvw * resMinusOne / res + 0.5 / res;
	float nz          = res.z;
	float paddedSlices = nz + 2.0;
	float atlasDepth  = 7.0 * paddedSlices;
	float uvZBase     = uvw.z * nz + 1.0;
	vec4 s0 = texture( probesSH, vec3( uvw.xy, ( uvZBase                       ) / atlasDepth ) );
	vec4 s1 = texture( probesSH, vec3( uvw.xy, ( uvZBase +       paddedSlices   ) / atlasDepth ) );
	vec4 s2 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 2.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s3 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 3.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s4 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 4.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s5 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 5.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s6 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 6.0 * paddedSlices   ) / atlasDepth ) );
	vec3 c0 = s0.xyz;
	vec3 c1 = vec3( s0.w, s1.xy );
	vec3 c2 = vec3( s1.zw, s2.x );
	vec3 c3 = s2.yzw;
	vec3 c4 = s3.xyz;
	vec3 c5 = vec3( s3.w, s4.xy );
	vec3 c6 = vec3( s4.zw, s5.x );
	vec3 c7 = s5.yzw;
	vec3 c8 = s6.xyz;
	float x = worldNormal.x, y = worldNormal.y, z = worldNormal.z;
	vec3 result = c0 * 0.886227;
	result += c1 * 2.0 * 0.511664 * y;
	result += c2 * 2.0 * 0.511664 * z;
	result += c3 * 2.0 * 0.511664 * x;
	result += c4 * 2.0 * 0.429043 * x * y;
	result += c5 * 2.0 * 0.429043 * y * z;
	result += c6 * ( 0.743125 * z * z - 0.247708 );
	result += c7 * 2.0 * 0.429043 * x * z;
	result += c8 * 0.429043 * ( x * x - y * y );
	return max( result, vec3( 0.0 ) );
}
#endif`,dv=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,fv=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,pv=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,mv=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,gv=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,_v=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,xv=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,vv=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,yv=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Mv=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Ev=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,bv=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Tv=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Sv=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,wv=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Av=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#ifdef DOUBLE_SIDED
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#ifdef DOUBLE_SIDED
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,Rv=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#if defined( USE_PACKED_NORMALMAP )
		mapN = vec3( mapN.xy, sqrt( saturate( 1.0 - dot( mapN.xy, mapN.xy ) ) ) );
	#endif
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,Cv=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Iv=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Pv=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
		#ifdef FLIP_SIDED
			vBitangent = - vBitangent;
		#endif
	#endif
#endif`,Lv=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,Dv=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,Nv=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,Uv=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Fv=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,Ov=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Bv=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	#ifdef USE_REVERSED_DEPTH_BUFFER
	
		return depth * ( far - near ) - far;
	#else
		return depth * ( near - far ) - near;
	#endif
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	
	#ifdef USE_REVERSED_DEPTH_BUFFER
		return ( near * far ) / ( ( near - far ) * depth - near );
	#else
		return ( near * far ) / ( ( far - near ) * depth - far );
	#endif
}`,Hv=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,kv=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Vv=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,zv=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Gv=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Wv=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Xv=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
		#define SUN_LIGHT_CASCADES 2
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow sunShadowMap[ NUM_SUN_LIGHT_SHADOWS ];
		#else
			uniform sampler2D sunShadowMap[ NUM_SUN_LIGHT_SHADOWS ];
		#endif
		uniform mat4 sunShadowMatrix[ NUM_SUN_LIGHT_SHADOWS * SUN_LIGHT_CASCADES ];
		uniform vec4 sunShadowCascade[ NUM_SUN_LIGHT_SHADOWS * SUN_LIGHT_CASCADES ];
		varying vec4 vSunShadowWorldPosition;
		varying vec3 vSunShadowWorldNormal;
		struct SunLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SunLightShadow sunLightShadows[ NUM_SUN_LIGHT_SHADOWS ];
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#else
			uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#endif
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#else
			uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#endif
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform samplerCubeShadow pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#elif defined( SHADOWMAP_TYPE_BASIC )
			uniform samplerCube pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#endif
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float interleavedGradientNoise( vec2 position ) {
			return fract( 52.9829189 * fract( dot( position, vec2( 0.06711056, 0.00583715 ) ) ) );
		}
		vec2 vogelDiskSample( int sampleIndex, int samplesCount, float phi ) {
			const float goldenAngle = 2.399963229728653;
			float r = sqrt( ( float( sampleIndex ) + 0.5 ) / float( samplesCount ) );
			float theta = float( sampleIndex ) * goldenAngle + phi;
			return vec2( cos( theta ), sin( theta ) ) * r;
		}
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float getShadow( sampler2DShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
				float radius = shadowRadius * texelSize.x;
				float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
				shadow = (
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 0, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 1, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 2, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 3, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 4, 5, phi ) * radius, shadowCoord.z ) )
				) * 0.2;
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#elif defined( SHADOWMAP_TYPE_VSM )
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 distribution = texture2D( shadowMap, shadowCoord.xy ).rg;
				float mean = distribution.x;
				float variance = distribution.y * distribution.y;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					float hard_shadow = step( mean, shadowCoord.z );
				#else
					float hard_shadow = step( shadowCoord.z, mean );
				#endif
				
				if ( hard_shadow == 1.0 ) {
					shadow = 1.0;
				} else {
					variance = max( variance, 0.0000001 );
					float d = shadowCoord.z - mean;
					float p_max = variance / ( variance + d * d );
					p_max = clamp( ( p_max - 0.3 ) / 0.65, 0.0, 1.0 );
					shadow = max( hard_shadow, p_max );
				}
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#else
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				float depth = texture2D( shadowMap, shadowCoord.xy ).r;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					shadow = step( depth, shadowCoord.z );
				#else
					shadow = step( shadowCoord.z, depth );
				#endif
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#endif
	#if NUM_SUN_LIGHT_SHADOWS > 0
		float getSunShadow(
			#if defined( SHADOWMAP_TYPE_PCF )
				sampler2DShadow shadowMap,
			#else
				sampler2D shadowMap,
			#endif
			SunLightShadow sunLightShadow,
			int shadowIndex
		) {
			vec4 shadowWorldPosition = vec4( vSunShadowWorldPosition.xyz + vSunShadowWorldNormal * sunLightShadow.shadowNormalBias, 1.0 );
			float viewDepth = vSunShadowWorldPosition.w;
			int cascadeOffset = shadowIndex * SUN_LIGHT_CASCADES;
			float shadow = 1.0;
			for ( int i = SUN_LIGHT_CASCADES - 1; i >= 0; i -- ) {
				vec4 cascade = sunShadowCascade[ cascadeOffset + i ];
				if ( viewDepth >= cascade.x && viewDepth < cascade.y ) {
					float cascadeShadow = getShadow(
						shadowMap,
						sunLightShadow.shadowMapSize,
						sunLightShadow.shadowIntensity,
						sunLightShadow.shadowBias,
						sunLightShadow.shadowRadius,
						sunShadowMatrix[ cascadeOffset + i ] * shadowWorldPosition
					);
					shadow = mix( cascadeShadow, shadow, smoothstep( cascade.z, cascade.y, viewDepth ) );
				}
			}
			return shadow;
		}
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	#if defined( SHADOWMAP_TYPE_PCF )
	float getPointShadow( samplerCubeShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 bd3D = normalize( lightToPosition );
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			#ifdef USE_REVERSED_DEPTH_BUFFER
				float dp = ( shadowCameraNear * ( shadowCameraFar - viewSpaceZ ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp -= shadowBias;
			#else
				float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp += shadowBias;
			#endif
			float texelSize = shadowRadius / shadowMapSize.x;
			vec3 absDir = abs( bd3D );
			vec3 tangent = absDir.x > absDir.z ? vec3( 0.0, 1.0, 0.0 ) : vec3( 1.0, 0.0, 0.0 );
			tangent = normalize( cross( bd3D, tangent ) );
			vec3 bitangent = cross( bd3D, tangent );
			float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
			vec2 sample0 = vogelDiskSample( 0, 5, phi );
			vec2 sample1 = vogelDiskSample( 1, 5, phi );
			vec2 sample2 = vogelDiskSample( 2, 5, phi );
			vec2 sample3 = vogelDiskSample( 3, 5, phi );
			vec2 sample4 = vogelDiskSample( 4, 5, phi );
			shadow = (
				texture( shadowMap, vec4( bd3D + ( tangent * sample0.x + bitangent * sample0.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample1.x + bitangent * sample1.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample2.x + bitangent * sample2.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample3.x + bitangent * sample3.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample4.x + bitangent * sample4.y ) * texelSize, dp ) )
			) * 0.2;
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#elif defined( SHADOWMAP_TYPE_BASIC )
	float getPointShadow( samplerCube shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			float depth = textureCube( shadowMap, bd3D ).r;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				depth = 1.0 - depth;
			#endif
			shadow = step( dp, depth );
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#endif
	#endif
#endif`,qv=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
		varying vec4 vSunShadowWorldPosition;
		varying vec3 vSunShadowWorldNormal;
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,Yv=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_SUN_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	#ifdef HAS_NORMAL
		vec3 shadowWorldNormal = transformNormalByInverseViewMatrix( transformedNormal, viewMatrix );
	#else
		vec3 shadowWorldNormal = vec3( 0.0 );
	#endif
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_SUN_LIGHT_SHADOWS > 0
		vSunShadowWorldPosition = vec4( worldPosition.xyz, - mvPosition.z );
		vSunShadowWorldNormal = shadowWorldNormal;
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,$v=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
	SunLightShadow sunLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SUN_LIGHT_SHADOWS; i ++ ) {
		sunLight = sunLightShadows[ i ];
		shadow *= receiveShadow ? getSunShadow( sunShadowMap[ i ], sunLight, UNROLLED_LOOP_INDEX ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0 && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,Zv=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,Kv=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,jv=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,Jv=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,Qv=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,ey=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,ty=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,ny=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,iy=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = transformNormalByInverseViewMatrix( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseContribution, material.specularColorBlended, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,sy=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,ry=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,oy=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,ay=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,ly=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,cy=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,hy=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,uy=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,dy=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vWorldDirection );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,fy=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,py=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,my=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,gy=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSED_DEPTH_BUFFER
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,_y=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,xy=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = vec4( dist, 0.0, 0.0, 1.0 );
}`,vy=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,yy=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,My=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Ey=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,by=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,Ty=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Sy=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,wy=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Ay=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,Ry=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Cy=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,Iy=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( normalize( normal ) * 0.5 + 0.5, diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,Py=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Ly=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Dy=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,Ny=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_RETROREFLECTION
	uniform float retroreflectivity;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
 
		outgoingLight = outgoingLight + sheenSpecularDirect + sheenSpecularIndirect;
 
 	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Uy=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Fy=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Oy=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,By=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Hy=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,ky=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Vy=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,zy=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,At={alphahash_fragment:cx,alphahash_pars_fragment:hx,alphamap_fragment:ux,alphamap_pars_fragment:dx,alphatest_fragment:fx,alphatest_pars_fragment:px,aomap_fragment:mx,aomap_pars_fragment:gx,batching_pars_vertex:_x,batching_vertex:xx,begin_vertex:vx,beginnormal_vertex:yx,bsdfs:Mx,iridescence_fragment:Ex,bumpmap_pars_fragment:bx,clipping_planes_fragment:Tx,clipping_planes_pars_fragment:Sx,clipping_planes_pars_vertex:wx,clipping_planes_vertex:Ax,color_fragment:Rx,color_pars_fragment:Cx,color_pars_vertex:Ix,color_vertex:Px,common:Lx,cube_uv_reflection_fragment:Dx,defaultnormal_vertex:Nx,displacementmap_pars_vertex:Ux,displacementmap_vertex:Fx,emissivemap_fragment:Ox,emissivemap_pars_fragment:Bx,colorspace_fragment:Hx,colorspace_pars_fragment:kx,envmap_fragment:Vx,envmap_common_pars_fragment:zx,envmap_pars_fragment:Gx,envmap_pars_vertex:Wx,envmap_physical_pars_fragment:tv,envmap_vertex:Xx,fog_vertex:qx,fog_pars_vertex:Yx,fog_fragment:$x,fog_pars_fragment:Zx,gradientmap_pars_fragment:Kx,lightmap_pars_fragment:jx,lights_lambert_fragment:Jx,lights_lambert_pars_fragment:Qx,lights_pars_begin:ev,lights_toon_fragment:nv,lights_toon_pars_fragment:iv,lights_phong_fragment:sv,lights_phong_pars_fragment:rv,lights_physical_fragment:ov,lights_physical_pars_fragment:av,lights_fragment_begin:lv,lights_fragment_maps:cv,lights_fragment_end:hv,lightprobes_pars_fragment:uv,logdepthbuf_fragment:dv,logdepthbuf_pars_fragment:fv,logdepthbuf_pars_vertex:pv,logdepthbuf_vertex:mv,map_fragment:gv,map_pars_fragment:_v,map_particle_fragment:xv,map_particle_pars_fragment:vv,metalnessmap_fragment:yv,metalnessmap_pars_fragment:Mv,morphinstance_vertex:Ev,morphcolor_vertex:bv,morphnormal_vertex:Tv,morphtarget_pars_vertex:Sv,morphtarget_vertex:wv,normal_fragment_begin:Av,normal_fragment_maps:Rv,normal_pars_fragment:Cv,normal_pars_vertex:Iv,normal_vertex:Pv,normalmap_pars_fragment:Lv,clearcoat_normal_fragment_begin:Dv,clearcoat_normal_fragment_maps:Nv,clearcoat_pars_fragment:Uv,iridescence_pars_fragment:Fv,opaque_fragment:Ov,packing:Bv,premultiplied_alpha_fragment:Hv,project_vertex:kv,dithering_fragment:Vv,dithering_pars_fragment:zv,roughnessmap_fragment:Gv,roughnessmap_pars_fragment:Wv,shadowmap_pars_fragment:Xv,shadowmap_pars_vertex:qv,shadowmap_vertex:Yv,shadowmask_pars_fragment:$v,skinbase_vertex:Zv,skinning_pars_vertex:Kv,skinning_vertex:jv,skinnormal_vertex:Jv,specularmap_fragment:Qv,specularmap_pars_fragment:ey,tonemapping_fragment:ty,tonemapping_pars_fragment:ny,transmission_fragment:iy,transmission_pars_fragment:sy,uv_pars_fragment:ry,uv_pars_vertex:oy,uv_vertex:ay,worldpos_vertex:ly,background_vert:cy,background_frag:hy,backgroundCube_vert:uy,backgroundCube_frag:dy,cube_vert:fy,cube_frag:py,depth_vert:my,depth_frag:gy,distance_vert:_y,distance_frag:xy,equirect_vert:vy,equirect_frag:yy,linedashed_vert:My,linedashed_frag:Ey,meshbasic_vert:by,meshbasic_frag:Ty,meshlambert_vert:Sy,meshlambert_frag:wy,meshmatcap_vert:Ay,meshmatcap_frag:Ry,meshnormal_vert:Cy,meshnormal_frag:Iy,meshphong_vert:Py,meshphong_frag:Ly,meshphysical_vert:Dy,meshphysical_frag:Ny,meshtoon_vert:Uy,meshtoon_frag:Fy,points_vert:Oy,points_frag:By,shadow_vert:Hy,shadow_frag:ky,sprite_vert:Vy,sprite_frag:zy},Be={common:{diffuse:{value:new ke(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new gt},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new gt}},envmap:{envMap:{value:null},envMapRotation:{value:new gt},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98},dfgLUT:{value:null}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new gt}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new gt}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new gt},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new gt},normalScale:{value:new Pe(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new gt},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new gt}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new gt}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new gt}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ke(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},sunLights:{value:[],properties:{direction:{},color:{}}},sunLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},sunShadowMatrix:{value:[]},sunShadowCascade:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null},probesSH:{value:null},probesMin:{value:new y},probesMax:{value:new y},probesResolution:{value:new y}},points:{diffuse:{value:new ke(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0},uvTransform:{value:new gt}},sprite:{diffuse:{value:new ke(16777215)},opacity:{value:1},center:{value:new Pe(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new gt},alphaMap:{value:null},alphaMapTransform:{value:new gt},alphaTest:{value:0}}},Ss={basic:{uniforms:$n([Be.common,Be.specularmap,Be.envmap,Be.aomap,Be.lightmap,Be.fog]),vertexShader:At.meshbasic_vert,fragmentShader:At.meshbasic_frag},lambert:{uniforms:$n([Be.common,Be.specularmap,Be.envmap,Be.aomap,Be.lightmap,Be.emissivemap,Be.bumpmap,Be.normalmap,Be.displacementmap,Be.fog,Be.lights,{emissive:{value:new ke(0)},envMapIntensity:{value:1}}]),vertexShader:At.meshlambert_vert,fragmentShader:At.meshlambert_frag},phong:{uniforms:$n([Be.common,Be.specularmap,Be.envmap,Be.aomap,Be.lightmap,Be.emissivemap,Be.bumpmap,Be.normalmap,Be.displacementmap,Be.fog,Be.lights,{emissive:{value:new ke(0)},specular:{value:new ke(1118481)},shininess:{value:30},envMapIntensity:{value:1}}]),vertexShader:At.meshphong_vert,fragmentShader:At.meshphong_frag},standard:{uniforms:$n([Be.common,Be.envmap,Be.aomap,Be.lightmap,Be.emissivemap,Be.bumpmap,Be.normalmap,Be.displacementmap,Be.roughnessmap,Be.metalnessmap,Be.fog,Be.lights,{emissive:{value:new ke(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:At.meshphysical_vert,fragmentShader:At.meshphysical_frag},toon:{uniforms:$n([Be.common,Be.aomap,Be.lightmap,Be.emissivemap,Be.bumpmap,Be.normalmap,Be.displacementmap,Be.gradientmap,Be.fog,Be.lights,{emissive:{value:new ke(0)}}]),vertexShader:At.meshtoon_vert,fragmentShader:At.meshtoon_frag},matcap:{uniforms:$n([Be.common,Be.bumpmap,Be.normalmap,Be.displacementmap,Be.fog,{matcap:{value:null}}]),vertexShader:At.meshmatcap_vert,fragmentShader:At.meshmatcap_frag},points:{uniforms:$n([Be.points,Be.fog]),vertexShader:At.points_vert,fragmentShader:At.points_frag},dashed:{uniforms:$n([Be.common,Be.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:At.linedashed_vert,fragmentShader:At.linedashed_frag},depth:{uniforms:$n([Be.common,Be.displacementmap]),vertexShader:At.depth_vert,fragmentShader:At.depth_frag},normal:{uniforms:$n([Be.common,Be.bumpmap,Be.normalmap,Be.displacementmap,{opacity:{value:1}}]),vertexShader:At.meshnormal_vert,fragmentShader:At.meshnormal_frag},sprite:{uniforms:$n([Be.sprite,Be.fog]),vertexShader:At.sprite_vert,fragmentShader:At.sprite_frag},background:{uniforms:{uvTransform:{value:new gt},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:At.background_vert,fragmentShader:At.background_frag},backgroundCube:{uniforms:{envMap:{value:null},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new gt}},vertexShader:At.backgroundCube_vert,fragmentShader:At.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:At.cube_vert,fragmentShader:At.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:At.equirect_vert,fragmentShader:At.equirect_frag},distance:{uniforms:$n([Be.common,Be.displacementmap,{referencePosition:{value:new y},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:At.distance_vert,fragmentShader:At.distance_frag},shadow:{uniforms:$n([Be.lights,Be.fog,{color:{value:new ke(0)},opacity:{value:1}}]),vertexShader:At.shadow_vert,fragmentShader:At.shadow_frag}};Ss.physical={uniforms:$n([Ss.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new gt},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new gt},clearcoatNormalScale:{value:new Pe(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new gt},dispersion:{value:0},retroreflectivity:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new gt},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new gt},sheen:{value:0},sheenColor:{value:new ke(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new gt},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new gt},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new gt},transmissionSamplerSize:{value:new Pe},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new gt},attenuationDistance:{value:0},attenuationColor:{value:new ke(0)},specularColor:{value:new ke(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new gt},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new gt},anisotropyVector:{value:new Pe},anisotropyMap:{value:null},anisotropyMapTransform:{value:new gt}}]),vertexShader:At.meshphysical_vert,fragmentShader:At.meshphysical_frag};var au={r:0,b:0,g:0},Gy=new rt,P0=new gt;P0.set(-1,0,0,0,1,0,0,0,1);function Wy(n,e,t,i,s,r){let o=new ke(0),a=s===!0?0:1,c,l,u=null,d=0,f=null;function p(A){let U=A.isScene===!0?A.background:null;if(U&&U.isTexture){let T=A.backgroundBlurriness>0;U=e.get(U,T)}return U}function x(A){let U=!1,T=p(A);T===null?g(o,a):T&&T.isColor&&(g(T,1),U=!0);let I=n.xr.getEnvironmentBlendMode();I==="additive"?t.buffers.color.setClear(0,0,0,1,r):I==="alpha-blend"&&t.buffers.color.setClear(0,0,0,0,r),(n.autoClear||U)&&(t.buffers.depth.setTest(!0),t.buffers.depth.setMask(!0),t.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function b(A,U){let T=p(U);T&&(T.isCubeTexture||T.mapping===El)?(l===void 0&&(l=new dn(new _t(1,1,1),new Un({name:"BackgroundCubeMaterial",uniforms:io(Ss.backgroundCube.uniforms),vertexShader:Ss.backgroundCube.vertexShader,fragmentShader:Ss.backgroundCube.fragmentShader,side:Hn,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),l.geometry.deleteAttribute("normal"),l.geometry.deleteAttribute("uv"),l.onBeforeRender=function(I,L,P){this.matrixWorld.copyPosition(P.matrixWorld)},Object.defineProperty(l.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),i.update(l)),l.material.uniforms.envMap.value=T,l.material.uniforms.backgroundBlurriness.value=U.backgroundBlurriness,l.material.uniforms.backgroundIntensity.value=U.backgroundIntensity,l.material.uniforms.backgroundRotation.value.setFromMatrix4(Gy.makeRotationFromEuler(U.backgroundRotation)).transpose(),T.isCubeTexture&&T.isRenderTargetTexture===!1&&l.material.uniforms.backgroundRotation.value.premultiply(P0),l.material.toneMapped=It.getTransfer(T.colorSpace)!==Gt,(u!==T||d!==T.version||f!==n.toneMapping)&&(l.material.needsUpdate=!0,u=T,d=T.version,f=n.toneMapping),l.layers.enableAll(),A.unshift(l,l.geometry,l.material,0,0,null)):T&&T.isTexture&&(c===void 0&&(c=new dn(new cn(2,2),new Un({name:"BackgroundMaterial",uniforms:io(Ss.background.uniforms),vertexShader:Ss.background.vertexShader,fragmentShader:Ss.background.fragmentShader,side:Es,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),c.geometry.deleteAttribute("normal"),Object.defineProperty(c.material,"map",{get:function(){return this.uniforms.t2D.value}}),i.update(c)),c.material.uniforms.t2D.value=T,c.material.uniforms.backgroundIntensity.value=U.backgroundIntensity,c.material.toneMapped=It.getTransfer(T.colorSpace)!==Gt,T.matrixAutoUpdate===!0&&T.updateMatrix(),c.material.uniforms.uvTransform.value.copy(T.matrix),(u!==T||d!==T.version||f!==n.toneMapping)&&(c.material.needsUpdate=!0,u=T,d=T.version,f=n.toneMapping),c.layers.enableAll(),A.unshift(c,c.geometry,c.material,0,0,null))}function g(A,U){A.getRGB(au,Zd(n)),t.buffers.color.setClear(au.r,au.g,au.b,U,r)}function m(){l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0),c!==void 0&&(c.geometry.dispose(),c.material.dispose(),c=void 0)}return{getClearColor:function(){return o},setClearColor:function(A,U=1){o.set(A),a=U,g(o,a)},getClearAlpha:function(){return a},setClearAlpha:function(A){a=A,g(o,a)},render:x,addToRenderList:b,dispose:m}}function Xy(n,e){let t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},s=f(null),r=s,o=!1;function a(H,k,q,z,ee){let he=!1,ue=d(H,z,q,k);r!==ue&&(r=ue,l(r.object)),he=p(H,z,q,ee),he&&x(H,z,q,ee),ee!==null&&e.update(ee,n.ELEMENT_ARRAY_BUFFER),(he||o)&&(o=!1,T(H,k,q,z),ee!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(ee).buffer))}function c(){return n.createVertexArray()}function l(H){return n.bindVertexArray(H)}function u(H){return n.deleteVertexArray(H)}function d(H,k,q,z){let ee=z.wireframe===!0,he=i[k.id];he===void 0&&(he={},i[k.id]=he);let ue=H.isInstancedMesh===!0?H.id:0,ye=he[ue];ye===void 0&&(ye={},he[ue]=ye);let V=ye[q.id];V===void 0&&(V={},ye[q.id]=V);let Q=V[ee];return Q===void 0&&(Q=f(c()),V[ee]=Q),Q}function f(H){let k=[],q=[],z=[];for(let ee=0;ee<t;ee++)k[ee]=0,q[ee]=0,z[ee]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:k,enabledAttributes:q,attributeDivisors:z,object:H,attributes:{},index:null}}function p(H,k,q,z){let ee=r.attributes,he=k.attributes,ue=0,ye=q.getAttributes();for(let V in ye)if(ye[V].location>=0){let le=ee[V],Ee=he[V];if(Ee===void 0&&(V==="instanceMatrix"&&H.instanceMatrix&&(Ee=H.instanceMatrix),V==="instanceColor"&&H.instanceColor&&(Ee=H.instanceColor)),le===void 0||le.attribute!==Ee||Ee&&le.data!==Ee.data)return!0;ue++}return r.attributesNum!==ue||r.index!==z}function x(H,k,q,z){let ee={},he=k.attributes,ue=0,ye=q.getAttributes();for(let V in ye)if(ye[V].location>=0){let le=he[V];le===void 0&&(V==="instanceMatrix"&&H.instanceMatrix&&(le=H.instanceMatrix),V==="instanceColor"&&H.instanceColor&&(le=H.instanceColor));let Ee={};Ee.attribute=le,le&&le.data&&(Ee.data=le.data),ee[V]=Ee,ue++}r.attributes=ee,r.attributesNum=ue,r.index=z}function b(){let H=r.newAttributes;for(let k=0,q=H.length;k<q;k++)H[k]=0}function g(H){m(H,0)}function m(H,k){let q=r.newAttributes,z=r.enabledAttributes,ee=r.attributeDivisors;q[H]=1,z[H]===0&&(n.enableVertexAttribArray(H),z[H]=1),ee[H]!==k&&(n.vertexAttribDivisor(H,k),ee[H]=k)}function A(){let H=r.newAttributes,k=r.enabledAttributes;for(let q=0,z=k.length;q<z;q++)k[q]!==H[q]&&(n.disableVertexAttribArray(q),k[q]=0)}function U(H,k,q,z,ee,he,ue){ue===!0?n.vertexAttribIPointer(H,k,q,ee,he):n.vertexAttribPointer(H,k,q,z,ee,he)}function T(H,k,q,z){b();let ee=z.attributes,he=q.getAttributes(),ue=k.defaultAttributeValues;for(let ye in he){let V=he[ye];if(V.location>=0){let Q=ee[ye];if(Q===void 0&&(ye==="instanceMatrix"&&H.instanceMatrix&&(Q=H.instanceMatrix),ye==="instanceColor"&&H.instanceColor&&(Q=H.instanceColor)),Q!==void 0){let le=Q.normalized,Ee=Q.itemSize,be=e.get(Q);if(be===void 0)continue;let ut=be.buffer,et=be.type,ct=be.bytesPerElement,ae=et===n.INT||et===n.UNSIGNED_INT||Q.gpuType===yh;if(Q.isInterleavedBufferAttribute){let me=Q.data,qe=me.stride,ft=Q.offset;if(me.isInstancedInterleavedBuffer){for(let Ge=0;Ge<V.locationSize;Ge++)m(V.location+Ge,me.meshPerAttribute);H.isInstancedMesh!==!0&&z._maxInstanceCount===void 0&&(z._maxInstanceCount=me.meshPerAttribute*me.count)}else for(let Ge=0;Ge<V.locationSize;Ge++)g(V.location+Ge);n.bindBuffer(n.ARRAY_BUFFER,ut);for(let Ge=0;Ge<V.locationSize;Ge++)U(V.location+Ge,Ee/V.locationSize,et,le,qe*ct,(ft+Ee/V.locationSize*Ge)*ct,ae)}else{if(Q.isInstancedBufferAttribute){for(let me=0;me<V.locationSize;me++)m(V.location+me,Q.meshPerAttribute);H.isInstancedMesh!==!0&&z._maxInstanceCount===void 0&&(z._maxInstanceCount=Q.meshPerAttribute*Q.count)}else for(let me=0;me<V.locationSize;me++)g(V.location+me);n.bindBuffer(n.ARRAY_BUFFER,ut);for(let me=0;me<V.locationSize;me++)U(V.location+me,Ee/V.locationSize,et,le,Ee*ct,Ee/V.locationSize*me*ct,ae)}}else if(ue!==void 0){let le=ue[ye];if(le!==void 0)switch(le.length){case 2:n.vertexAttrib2fv(V.location,le);break;case 3:n.vertexAttrib3fv(V.location,le);break;case 4:n.vertexAttrib4fv(V.location,le);break;default:n.vertexAttrib1fv(V.location,le)}}}}A()}function I(){C();for(let H in i){let k=i[H];for(let q in k){let z=k[q];for(let ee in z){let he=z[ee];for(let ue in he)u(he[ue].object),delete he[ue];delete z[ee]}}delete i[H]}}function L(H){if(i[H.id]===void 0)return;let k=i[H.id];for(let q in k){let z=k[q];for(let ee in z){let he=z[ee];for(let ue in he)u(he[ue].object),delete he[ue];delete z[ee]}}delete i[H.id]}function P(H){for(let k in i){let q=i[k];for(let z in q){let ee=q[z];if(ee[H.id]===void 0)continue;let he=ee[H.id];for(let ue in he)u(he[ue].object),delete he[ue];delete ee[H.id]}}}function M(H){for(let k in i){let q=i[k],z=H.isInstancedMesh===!0?H.id:0,ee=q[z];if(ee!==void 0){for(let he in ee){let ue=ee[he];for(let ye in ue)u(ue[ye].object),delete ue[ye];delete ee[he]}delete q[z],Object.keys(q).length===0&&delete i[k]}}}function C(){O(),o=!0,r!==s&&(r=s,l(r.object))}function O(){s.geometry=null,s.program=null,s.wireframe=!1}return{setup:a,reset:C,resetDefaultState:O,dispose:I,releaseStatesOfGeometry:L,releaseStatesOfObject:M,releaseStatesOfProgram:P,initAttributes:b,enableAttribute:g,disableUnusedAttributes:A}}function qy(n,e,t){let i;function s(c){i=c}function r(c,l){n.drawArrays(i,c,l),t.update(l,i,1)}function o(c,l,u){u!==0&&(n.drawArraysInstanced(i,c,l,u),t.update(l,i,u))}function a(c,l,u){if(u===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,c,0,l,0,u);let f=0;for(let p=0;p<u;p++)f+=l[p];t.update(f,i,1)}this.setMode=s,this.render=r,this.renderInstances=o,this.renderMultiDraw=a}function Yy(n,e,t,i){let s;function r(){if(s!==void 0)return s;if(e.has("EXT_texture_filter_anisotropic")===!0){let P=e.get("EXT_texture_filter_anisotropic");s=n.getParameter(P.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else s=0;return s}function o(P){return!(P!==Si&&i.convert(P)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function a(P){let M=P===rs&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(P!==di&&P!==Ti&&!M&&i.convert(P)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE))}function c(P){if(P==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";P="mediump"}return P==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp",u=c(l);u!==l&&(nt("WebGLRenderer:",l,"not supported, using",u,"instead."),l=u);let d=t.logarithmicDepthBuffer===!0,f=t.reversedDepthBuffer===!0&&e.has("EXT_clip_control");t.reversedDepthBuffer===!0&&f===!1&&nt("WebGLRenderer: Unable to use reversed depth buffer due to missing EXT_clip_control extension. Fallback to default depth buffer.");let p=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),x=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),b=n.getParameter(n.MAX_TEXTURE_SIZE),g=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),m=n.getParameter(n.MAX_VERTEX_ATTRIBS),A=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),U=n.getParameter(n.MAX_VARYING_VECTORS),T=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),I=n.getParameter(n.MAX_SAMPLES),L=n.getParameter(n.SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:r,getMaxPrecision:c,textureFormatReadable:o,textureTypeReadable:a,precision:l,logarithmicDepthBuffer:d,reversedDepthBuffer:f,maxTextures:p,maxVertexTextures:x,maxTextureSize:b,maxCubemapSize:g,maxAttributes:m,maxVertexUniforms:A,maxVaryings:U,maxFragmentUniforms:T,maxSamples:I,samples:L}}function $y(n){let e=this,t=null,i=0,s=!1,r=!1,o=new Bn,a=new gt,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(d,f){let p=d.length!==0||f||i!==0||s;return s=f,i=d.length,p},this.beginShadows=function(){r=!0,u(null)},this.endShadows=function(){r=!1},this.setGlobalState=function(d,f){t=u(d,f,0)},this.setState=function(d,f,p){let x=d.clippingPlanes,b=d.clipIntersection,g=d.clipShadows,m=n.get(d);if(!s||x===null||x.length===0||r&&!g)r?u(null):l();else{let A=r?0:i,U=A*4,T=m.clippingState||null;c.value=T,T=u(x,f,U,p);for(let I=0;I!==U;++I)T[I]=t[I];m.clippingState=T,this.numIntersection=b?this.numPlanes:0,this.numPlanes+=A}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function u(d,f,p,x){let b=d!==null?d.length:0,g=null;if(b!==0){if(g=c.value,x!==!0||g===null){let m=p+b*4,A=f.matrixWorldInverse;a.getNormalMatrix(A),(g===null||g.length<m)&&(g=new Float32Array(m));for(let U=0,T=p;U!==b;++U,T+=4)o.copy(d[U]).applyMatrix4(A,a),o.normal.toArray(g,T),g[T+3]=o.constant}c.value=g,c.needsUpdate=!0}return e.numPlanes=b,e.numIntersection=0,g}}var da=4,Zy=6,Ky=20,jy=256,Il=new mr,c0=new ke,Qd=null,ef=0,tf=0,nf=!1,Jy=new y,so=new y,pa=class{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._sizeLods=[],this._lodMeshes=[],this._backgroundBox=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._blurMaterial=null,this._ggxMaterial=null}fromScene(e,t=0,i=.1,s=100,r={}){let{size:o=256,position:a=Jy}=r;Qd=this._renderer.getRenderTarget(),ef=this._renderer.getActiveCubeFace(),tf=this._renderer.getActiveMipmapLevel(),nf=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(o);let c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,s,c,a),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=d0(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=u0(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose(),this._backgroundBox!==null&&(this._backgroundBox.geometry.dispose(),this._backgroundBox.material.dispose())}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._ggxMaterial!==null&&this._ggxMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodMeshes.length;e++)this._lodMeshes[e].geometry.dispose()}_cleanup(e){this._renderer.setRenderTarget(Qd,ef,tf),this._renderer.xr.enabled=nf,e.scissorTest=!1,ua(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===gr||e.mapping===to?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Qd=this._renderer.getRenderTarget(),ef=this._renderer.getActiveCubeFace(),tf=this._renderer.getActiveMipmapLevel(),nf=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;let i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){let e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:yn,minFilter:yn,generateMipmaps:!1,type:rs,format:Si,colorSpace:ti,depthBuffer:!1},s=h0(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=h0(e,t,i);let{_lodMax:r}=this;({lodMeshes:this._lodMeshes,sizeLods:this._sizeLods}=Qy(r)),this._blurMaterial=tM(r,e,t),this._ggxMaterial=eM(r,e,t)}return s}_compileMaterial(e){let t=new dn(new tn,e);this._renderer.compile(t,Il)}_sceneToCubeUV(e,t,i,s,r){let c=new An(90,1,t,i),l=[1,-1,1,1,1,1],u=[1,1,1,-1,-1,-1],d=this._renderer,f=d.autoClear,p=d.toneMapping;d.getClearColor(c0),d.toneMapping=ns,d.autoClear=!1,d.state.buffers.depth.getReversed()&&(d.setRenderTarget(s),d.clearDepth(),d.setRenderTarget(null)),this._backgroundBox===null&&(this._backgroundBox=new dn(new _t,new ln({name:"PMREM.Background",side:Hn,depthWrite:!1,depthTest:!1})));let b=this._backgroundBox,g=b.material,m=!1,A=e.background;A?A.isColor&&(g.color.copy(A),e.background=null,m=!0):(g.color.copy(c0),m=!0);for(let U=0;U<6;U++){let T=U%3;T===0?(c.up.set(0,l[U],0),c.position.set(r.x,r.y,r.z),c.lookAt(r.x+u[U],r.y,r.z)):T===1?(c.up.set(0,0,l[U]),c.position.set(r.x,r.y,r.z),c.lookAt(r.x,r.y+u[U],r.z)):(c.up.set(0,l[U],0),c.position.set(r.x,r.y,r.z),c.lookAt(r.x,r.y,r.z+u[U]));let I=this._cubeSize;ua(s,T*I,U>2?I:0,I,I),d.setRenderTarget(s),m&&d.render(b,c),d.render(e,c)}d.toneMapping=p,d.autoClear=f,e.background=A}_textureToCubeUV(e,t){let i=this._renderer,s=e.mapping===gr||e.mapping===to;s?(this._cubemapMaterial===null&&(this._cubemapMaterial=d0()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=u0());let r=s?this._cubemapMaterial:this._equirectMaterial,o=this._lodMeshes[0];o.material=r;let a=r.uniforms;a.envMap.value=e;let c=this._cubeSize;ua(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(o,Il)}_applyPMREM(e){let t=this._renderer,i=t.autoClear;t.autoClear=!1;let s=this._lodMeshes.length;for(let r=1;r<s;r++)this._applyGGXFilter(e,r-1,r);t.autoClear=i}_applyGGXFilter(e,t,i){let s=this._renderer,r=this._pingPongRenderTarget,o=this._ggxMaterial,a=this._lodMeshes[i];a.material=o;let c=o.uniforms,l=i/(this._lodMeshes.length-1),u=t/(this._lodMeshes.length-1),d=Math.sqrt(l*l-u*u),f=l*1.25,p=d*f,{_lodMax:x}=this,b=this._sizeLods[i],g=3*b*(i>x-da?i-x+da:0),m=4*(this._cubeSize-b);c.envMap.value=e.texture,c.roughness.value=p,c.mipInt.value=x-t,ua(r,g,m,3*b,2*b),s.setRenderTarget(r),s.render(a,Il),c.envMap.value=r.texture,c.roughness.value=0,c.mipInt.value=x-i,ua(e,g,m,3*b,2*b),s.setRenderTarget(e),s.render(a,Il)}_blur(e,t,i,s){let r=this._pingPongRenderTarget,o=Math.min(s,Math.PI)/Math.SQRT2;this._blurPass(e,r,t,i,o),this._blurPass(r,e,i,i,o)}_blurPass(e,t,i,s,r){let o=this._renderer,a=this._blurMaterial,c=this._lodMeshes[s];c.material=a;let l=a.uniforms;l.envMap.value=e.texture,l.sigma.value=r,l.mipInt.value=this._lodMax-i;let u=this._sizeLods[s],d=3*u*(s>this._lodMax-da?s-this._lodMax+da:0),f=4*(this._cubeSize-u);ua(t,d,f,3*u,2*u),o.setRenderTarget(t),o.render(c,Il)}};function Qy(n){let e=[],t=[],i=n,s=n-da+1+Zy;for(let r=0;r<s;r++){let o=Math.pow(2,i);e.push(o);let a=1/(o-2),c=-a,l=1+a,u=[c,c,l,c,l,l,c,c,l,l,c,l],d=6,f=6,p=3,x=new Float32Array(p*f*d),b=new Float32Array(p*f*d);for(let m=0;m<d;m++){let A=m%3*2/3-1,U=m>2?0:-1,T=[A,U,0,A+2/3,U,0,A+2/3,U+1,0,A,U,0,A+2/3,U+1,0,A,U+1,0];x.set(T,p*f*m);for(let I=0;I<f;I++){let L=u[I*2]*2-1,P=u[I*2+1]*2-1;m===0?so.set(1,P,L):m===1?so.set(-L,1,-P):m===2?so.set(-L,P,1):m===3?so.set(-1,P,-L):m===4?so.set(-L,-1,P):so.set(L,P,-1),so.toArray(b,(m*f+I)*p)}}let g=new tn;g.setAttribute("position",new Cn(x,p)),g.setAttribute("outputDirection",new Cn(b,p)),t.push(new dn(g,null)),i>da&&i--}return{lodMeshes:t,sizeLods:e}}function h0(n,e,t){let i=new ai(n,e,t);return i.texture.mapping=El,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function ua(n,e,t,i,s){n.viewport.set(e,t,i,s),n.scissor.set(e,t,i,s)}function eM(n,e,t){return new Un({name:"PMREMGGXConvolution",defines:{GGX_SAMPLES:jy,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},roughness:{value:0},mipInt:{value:0}},vertexShader:uu(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float roughness;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359

			// Van der Corput radical inverse
			float radicalInverse_VdC(uint bits) {
				bits = (bits << 16u) | (bits >> 16u);
				bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
				bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
				bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
				bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
				return float(bits) * 2.3283064365386963e-10; // / 0x100000000
			}

			// Hammersley sequence
			vec2 hammersley(uint i, uint N) {
				return vec2(float(i) / float(N), radicalInverse_VdC(i));
			}

			// GGX VNDF importance sampling (Eric Heitz 2018)
			// "Sampling the GGX Distribution of Visible Normals"
			// https://jcgt.org/published/0007/04/01/
			vec3 importanceSampleGGX_VNDF(vec2 Xi, vec3 V, float roughness) {
				float alpha = roughness * roughness;

				// Section 4.1: Orthonormal basis
				vec3 T1 = vec3(1.0, 0.0, 0.0);
				vec3 T2 = cross(V, T1);

				// Section 4.2: Parameterization of projected area
				float r = sqrt(Xi.x);
				float phi = 2.0 * PI * Xi.y;
				float t1 = r * cos(phi);
				float t2 = r * sin(phi);
				float s = 0.5 * (1.0 + V.z);
				t2 = (1.0 - s) * sqrt(1.0 - t1 * t1) + s * t2;

				// Section 4.3: Reprojection onto hemisphere
				vec3 Nh = t1 * T1 + t2 * T2 + sqrt(max(0.0, 1.0 - t1 * t1 - t2 * t2)) * V;

				// Section 3.4: Transform back to ellipsoid configuration
				return normalize(vec3(alpha * Nh.x, alpha * Nh.y, max(0.0, Nh.z)));
			}

			void main() {
				vec3 N = normalize(vOutputDirection);
				vec3 V = N; // Assume view direction equals normal for pre-filtering

				vec3 prefilteredColor = vec3(0.0);
				float totalWeight = 0.0;

				// For very low roughness, just sample the environment directly
				if (roughness < 0.001) {
					gl_FragColor = vec4(bilinearCubeUV(envMap, N, mipInt), 1.0);
					return;
				}

				// Tangent space basis for VNDF sampling
				vec3 up = abs(N.z) < 0.999 ? vec3(0.0, 0.0, 1.0) : vec3(1.0, 0.0, 0.0);
				vec3 tangent = normalize(cross(up, N));
				vec3 bitangent = cross(N, tangent);

				for(uint i = 0u; i < uint(GGX_SAMPLES); i++) {
					vec2 Xi = hammersley(i, uint(GGX_SAMPLES));

					// For PMREM, V = N, so in tangent space V is always (0, 0, 1)
					vec3 H_tangent = importanceSampleGGX_VNDF(Xi, vec3(0.0, 0.0, 1.0), roughness);

					// Transform H back to world space
					vec3 H = normalize(tangent * H_tangent.x + bitangent * H_tangent.y + N * H_tangent.z);
					vec3 L = normalize(2.0 * dot(V, H) * H - V);

					float NdotL = max(dot(N, L), 0.0);

					if(NdotL > 0.0) {
						// Sample environment at fixed mip level
						// VNDF importance sampling handles the distribution filtering
						vec3 sampleColor = bilinearCubeUV(envMap, L, mipInt);

						// Weight by NdotL for the split-sum approximation
						// VNDF PDF naturally accounts for the visible microfacet distribution
						prefilteredColor += sampleColor * NdotL;
						totalWeight += NdotL;
					}
				}

				if (totalWeight > 0.0) {
					prefilteredColor = prefilteredColor / totalWeight;
				}

				gl_FragColor = vec4(prefilteredColor, 1.0);
			}
		`,blending:bs,depthTest:!1,depthWrite:!1})}function tM(n,e,t){return new Un({name:"SphericalGaussianBlur",defines:{SAMPLES:Ky,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},sigma:{value:0},mipInt:{value:0}},vertexShader:uu(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float sigma;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359
			#define GOLDEN_ANGLE 2.39996322973

			void main() {

				if ( sigma == 0.0 ) {

					gl_FragColor = vec4( bilinearCubeUV( envMap, vOutputDirection, mipInt ), 1.0 );
					return;

				}

				vec3 outputDirection = normalize( vOutputDirection );

				vec3 up = abs( outputDirection.z ) < 0.999 ? vec3( 0.0, 0.0, 1.0 ) : vec3( 1.0, 0.0, 0.0 );
				vec3 tangent = normalize( cross( up, outputDirection ) );
				vec3 bitangent = cross( outputDirection, tangent );

				// Truncate the kernel at three standard deviations or at the antipode.
				float thetaMax = min( 3.0 * sigma, PI );
				float truncation = 1.0 - exp( - 0.5 * thetaMax * thetaMax / ( sigma * sigma ) );

				vec3 accumColor = vec3( 0.0 );
				float accumWeight = 0.0;

				for ( int i = 0; i < SAMPLES; i ++ ) {

					// Stratified inverse-CDF sampling of the Gaussian, placed on a golden-angle spiral.
					float stratum = ( float( i ) + 0.5 ) / float( SAMPLES );
					float theta = sigma * sqrt( - 2.0 * log( 1.0 - stratum * truncation ) );
					float phi = float( i ) * GOLDEN_ANGLE;

					vec3 offset = cos( phi ) * tangent + sin( phi ) * bitangent;
					vec3 sampleDirection = cos( theta ) * outputDirection + sin( theta ) * offset;

					// Correct the planar sample density to solid angle.
					float weight = sin( theta ) / theta;

					accumColor += weight * bilinearCubeUV( envMap, sampleDirection, mipInt );
					accumWeight += weight;

				}

				gl_FragColor = vec4( accumColor / accumWeight, 1.0 );

			}
		`,blending:bs,depthTest:!1,depthWrite:!1})}function u0(){return new Un({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:uu(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:bs,depthTest:!1,depthWrite:!1})}function d0(){return new Un({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:uu(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:bs,depthTest:!1,depthWrite:!1})}function uu(){return`

		precision mediump float;
		precision mediump int;

		attribute vec3 outputDirection;

		varying vec3 vOutputDirection;

		void main() {

			vOutputDirection = outputDirection;
			gl_Position = vec4( position, 1.0 );

		}
	`}var cu=class extends ai{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;let i={width:e,height:e,depth:1},s=[i,i,i,i,i,i];this.texture=new sl(s),this._setTextureOptions(t),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;let i={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},s=new _t(5,5,5),r=new Un({name:"CubemapFromEquirect",uniforms:io(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Hn,blending:bs});r.uniforms.tEquirect.value=t;let o=new dn(s,r),a=t.minFilter;return t.minFilter===is&&(t.minFilter=yn),new ph(1,10,this).update(e,o),t.minFilter=a,o.geometry.dispose(),o.material.dispose(),this}clear(e,t=!0,i=!0,s=!0){let r=e.getRenderTarget();for(let o=0;o<6;o++)e.setRenderTarget(this,o),e.clear(t,i,s);e.setRenderTarget(r)}};function nM(n){let e=new WeakMap,t=new WeakMap,i=null;function s(f,p=!1){return f==null?null:p?o(f):r(f)}function r(f){if(f&&f.isTexture){let p=f.mapping;if(p===_h||p===xh)if(e.has(f)){let x=e.get(f).texture;return a(x,f.mapping)}else{let x=f.image;if(x&&x.height>0){let b=new cu(x.height);return b.fromEquirectangularTexture(n,f),e.set(f,b),f.addEventListener("dispose",l),a(b.texture,f.mapping)}else return null}}return f}function o(f){if(f&&f.isTexture){let p=f.mapping,x=p===_h||p===xh,b=p===gr||p===to;if(x||b){let g=t.get(f),m=g!==void 0?g.texture.pmremVersion:0;if(f.isRenderTargetTexture&&f.pmremVersion!==m)return i===null&&(i=new pa(n)),g=x?i.fromEquirectangular(f,g):i.fromCubemap(f,g),g.texture.pmremVersion=f.pmremVersion,t.set(f,g),g.texture;if(g!==void 0)return g.texture;{let A=f.image;return x&&A&&A.height>0||b&&A&&c(A)?(i===null&&(i=new pa(n)),g=x?i.fromEquirectangular(f):i.fromCubemap(f),g.texture.pmremVersion=f.pmremVersion,t.set(f,g),f.addEventListener("dispose",u),g.texture):null}}}return f}function a(f,p){return p===_h?f.mapping=gr:p===xh&&(f.mapping=to),f}function c(f){let p=0,x=6;for(let b=0;b<x;b++)f[b]!==void 0&&p++;return p===x}function l(f){let p=f.target;p.removeEventListener("dispose",l);let x=e.get(p);x!==void 0&&(e.delete(p),x.dispose())}function u(f){let p=f.target;p.removeEventListener("dispose",u);let x=t.get(p);x!==void 0&&(t.delete(p),x.dispose())}function d(){e=new WeakMap,t=new WeakMap,i!==null&&(i.dispose(),i=null)}return{get:s,dispose:d}}function iM(n){let e={};function t(i){if(e[i]!==void 0)return e[i];let s=n.getExtension(i);return e[i]=s,s}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){let s=t(i);return s===null&&kr("WebGLRenderer: "+i+" extension not supported."),s}}}function sM(n,e,t,i){let s={},r=new WeakMap;function o(d){let f=d.target;f.index!==null&&e.remove(f.index);for(let x in f.attributes)e.remove(f.attributes[x]);f.removeEventListener("dispose",o),delete s[f.id];let p=r.get(f);p&&(e.remove(p),r.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function a(d,f){return s[f.id]===!0||(f.addEventListener("dispose",o),s[f.id]=!0,t.memory.geometries++),f}function c(d){let f=d.attributes;for(let p in f)e.update(f[p],n.ARRAY_BUFFER)}function l(d){let f=[],p=d.index,x=d.attributes.position,b=0;if(x===void 0)return;if(p!==null){let A=p.array;b=p.version;for(let U=0,T=A.length;U<T;U+=3){let I=A[U+0],L=A[U+1],P=A[U+2];f.push(I,L,L,P,P,I)}}else{let A=x.array;b=x.version;for(let U=0,T=A.length/3-1;U<T;U+=3){let I=U+0,L=U+1,P=U+2;f.push(I,L,L,P,P,I)}}let g=new(x.count>=65535?el:Qa)(f,1);g.version=b;let m=r.get(d);m&&e.remove(m),r.set(d,g)}function u(d){let f=r.get(d);if(f){let p=d.index;p!==null&&f.version<p.version&&l(d)}else l(d);return r.get(d)}return{get:a,update:c,getWireframeAttribute:u}}function rM(n,e,t){let i;function s(d){i=d}let r,o;function a(d){r=d.type,o=d.bytesPerElement}function c(d,f){n.drawElements(i,f,r,d*o),t.update(f,i,1)}function l(d,f,p){p!==0&&(n.drawElementsInstanced(i,f,r,d*o,p),t.update(f,i,p))}function u(d,f,p){if(p===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,f,0,r,d,0,p);let b=0;for(let g=0;g<p;g++)b+=f[g];t.update(b,i,1)}this.setMode=s,this.setIndex=a,this.render=c,this.renderInstances=l,this.renderMultiDraw=u}function oM(n){let e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(r,o,a){switch(t.calls++,o){case n.TRIANGLES:t.triangles+=a*(r/3);break;case n.LINES:t.lines+=a*(r/2);break;case n.LINE_STRIP:t.lines+=a*(r-1);break;case n.LINE_LOOP:t.lines+=a*r;break;case n.POINTS:t.points+=a*r;break;default:ht("WebGLInfo: Unknown draw mode:",o);break}}function s(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:s,update:i}}function aM(n,e,t){let i=new WeakMap,s=new $t;function r(o,a,c){let l=o.morphTargetInfluences,u=a.morphAttributes.position||a.morphAttributes.normal||a.morphAttributes.color,d=u!==void 0?u.length:0,f=i.get(a);if(f===void 0||f.count!==d){let C=function(){P.dispose(),i.delete(a),a.removeEventListener("dispose",C)};f!==void 0&&f.texture.dispose();let p=a.morphAttributes.position!==void 0,x=a.morphAttributes.normal!==void 0,b=a.morphAttributes.color!==void 0,g=a.morphAttributes.position||[],m=a.morphAttributes.normal||[],A=a.morphAttributes.color||[],U=0;p===!0&&(U=1),x===!0&&(U=2),b===!0&&(U=3);let T=a.attributes.position.count*U,I=1;T>e.maxTextureSize&&(I=Math.ceil(T/e.maxTextureSize),T=e.maxTextureSize);let L=new Float32Array(T*I*4*d),P=new Ja(L,T,I,d);P.type=Ti,P.needsUpdate=!0;let M=U*4;for(let O=0;O<d;O++){let H=g[O],k=m[O],q=A[O],z=T*I*4*O;for(let ee=0;ee<H.count;ee++){let he=ee*M;p===!0&&(s.fromBufferAttribute(H,ee),L[z+he+0]=s.x,L[z+he+1]=s.y,L[z+he+2]=s.z,L[z+he+3]=0),x===!0&&(s.fromBufferAttribute(k,ee),L[z+he+4]=s.x,L[z+he+5]=s.y,L[z+he+6]=s.z,L[z+he+7]=0),b===!0&&(s.fromBufferAttribute(q,ee),L[z+he+8]=s.x,L[z+he+9]=s.y,L[z+he+10]=s.z,L[z+he+11]=q.itemSize===4?s.w:1)}}f={count:d,texture:P,size:new Pe(T,I)},i.set(a,f),a.addEventListener("dispose",C)}if(o.isInstancedMesh===!0&&o.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",o.morphTexture,t);else{let p=0;for(let b=0;b<l.length;b++)p+=l[b];let x=a.morphTargetsRelative?1:1-p;c.getUniforms().setValue(n,"morphTargetBaseInfluence",x),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:r}}function lM(n,e,t,i,s){let r=new WeakMap;function o(l){let u=s.render.frame,d=l.geometry,f=e.get(l,d);if(r.get(f)!==u&&(e.update(f),r.set(f,u)),l.isInstancedMesh&&(l.hasEventListener("dispose",c)===!1&&l.addEventListener("dispose",c),r.get(l)!==u&&(t.update(l.instanceMatrix,n.ARRAY_BUFFER),l.instanceColor!==null&&t.update(l.instanceColor,n.ARRAY_BUFFER),r.set(l,u))),l.isSkinnedMesh){let p=l.skeleton;r.get(p)!==u&&(p.update(),r.set(p,u))}return f}function a(){r=new WeakMap}function c(l){let u=l.target;u.removeEventListener("dispose",c),i.releaseStatesOfObject(u),t.remove(u.instanceMatrix),u.instanceColor!==null&&t.remove(u.instanceColor)}return{update:o,dispose:a}}var cM={[Pd]:"LINEAR_TONE_MAPPING",[Ld]:"REINHARD_TONE_MAPPING",[Dd]:"CINEON_TONE_MAPPING",[Ml]:"ACES_FILMIC_TONE_MAPPING",[Ud]:"AGX_TONE_MAPPING",[Fd]:"NEUTRAL_TONE_MAPPING",[Nd]:"CUSTOM_TONE_MAPPING"};function hM(n,e,t,i,s,r){let o=new ai(e,t,{type:n,depthBuffer:s,stencilBuffer:r,samples:i?4:0,storeMultisampledDepthBuffer:!1,storeMultisampledStencilBuffer:!1,resolveDepthBuffer:!1,resolveStencilBuffer:!1}),a=null,c=null,l=new tn;l.setAttribute("position",new Dt([-1,3,0,-1,-1,0,3,-1,0],3)),l.setAttribute("uv",new Dt([0,2,0,0,2,0],2));let u=new sh({uniforms:{tDiffuse:{value:null}},vertexShader:`
			precision highp float;

			uniform mat4 modelViewMatrix;
			uniform mat4 projectionMatrix;

			attribute vec3 position;
			attribute vec2 uv;

			varying vec2 vUv;

			void main() {
				vUv = uv;
				gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			}`,fragmentShader:`
			precision highp float;

			uniform sampler2D tDiffuse;

			varying vec2 vUv;

			#include <tonemapping_pars_fragment>
			#include <colorspace_pars_fragment>

			void main() {
				gl_FragColor = texture2D( tDiffuse, vUv );

				#ifdef LINEAR_TONE_MAPPING
					gl_FragColor.rgb = LinearToneMapping( gl_FragColor.rgb );
				#elif defined( REINHARD_TONE_MAPPING )
					gl_FragColor.rgb = ReinhardToneMapping( gl_FragColor.rgb );
				#elif defined( CINEON_TONE_MAPPING )
					gl_FragColor.rgb = CineonToneMapping( gl_FragColor.rgb );
				#elif defined( ACES_FILMIC_TONE_MAPPING )
					gl_FragColor.rgb = ACESFilmicToneMapping( gl_FragColor.rgb );
				#elif defined( AGX_TONE_MAPPING )
					gl_FragColor.rgb = AgXToneMapping( gl_FragColor.rgb );
				#elif defined( NEUTRAL_TONE_MAPPING )
					gl_FragColor.rgb = NeutralToneMapping( gl_FragColor.rgb );
				#elif defined( CUSTOM_TONE_MAPPING )
					gl_FragColor.rgb = CustomToneMapping( gl_FragColor.rgb );
				#endif

				#ifdef SRGB_TRANSFER
					gl_FragColor = sRGBTransferOETF( gl_FragColor );
				#endif
			}`,depthTest:!1,depthWrite:!1}),d=new dn(l,u),f=new mr(-1,1,1,-1,0,1),p=null,x=null,b=!1,g,m=null,A=[],U=!1;this.setSize=function(T,I){o.setSize(T,I),a!==null&&a.setSize(T,I),c!==null&&c.setSize(T,I);for(let L=0;L<A.length;L++){let P=A[L];P.setSize&&P.setSize(T,I)}},this.setEffects=function(T){A=T,U=A.length>0&&A[0].isRenderPass===!0;let I=o.width,L=o.height;A.length>0&&a===null&&(a=new ai(I,L,{type:rs,depthBuffer:!1,stencilBuffer:!1}),c=new ai(I,L,{type:rs,depthBuffer:!1,stencilBuffer:!1}));for(let P=0;P<A.length;P++){let M=A[P];M.setSize&&M.setSize(I,L)}},this.begin=function(T,I){if(b||T.toneMapping===ns&&A.length===0)return!1;if(m=I,I!==null){let L=I.width,P=I.height;(o.width!==L||o.height!==P)&&this.setSize(L,P)}return U===!1&&T.setRenderTarget(o),g=T.toneMapping,T.toneMapping=ns,!0},this.hasRenderPass=function(){return U},this.end=function(T,I){T.toneMapping=g,b=!0;let L=o,P=a;for(let M=0;M<A.length;M++){let C=A[M];C.enabled!==!1&&(C.render(T,P,L,I),C.needsSwap!==!1&&(L=P,P=P===a?c:a))}if(p!==T.outputColorSpace||x!==T.toneMapping){p=T.outputColorSpace,x=T.toneMapping,u.defines={},It.getTransfer(p)===Gt&&(u.defines.SRGB_TRANSFER="");let M=cM[x];M&&(u.defines[M]=""),u.needsUpdate=!0}u.uniforms.tDiffuse.value=L.texture,T.setRenderTarget(m),T.render(d,f),m=null,b=!1},this.isCompositing=function(){return b},this.dispose=function(){o.dispose(),a!==null&&a.dispose(),c!==null&&c.dispose(),l.dispose(),u.dispose()}}var L0=new In,of=new dr(1,1),D0=new Ja,N0=new Yc,U0=new sl,f0=[],p0=[],m0=new Float32Array(16),g0=new Float32Array(9),_0=new Float32Array(4);function ma(n,e,t){let i=n[0];if(i<=0||i>0)return n;let s=e*t,r=f0[s];if(r===void 0&&(r=new Float32Array(s),f0[s]=r),e!==0){i.toArray(r,0);for(let o=1,a=0;o!==e;++o)a+=t,n[o].toArray(r,a)}return r}function Pn(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function Ln(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function du(n,e){let t=p0[e];t===void 0&&(t=new Int32Array(e),p0[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function uM(n,e){let t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function dM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Pn(t,e))return;n.uniform2fv(this.addr,e),Ln(t,e)}}function fM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(Pn(t,e))return;n.uniform3fv(this.addr,e),Ln(t,e)}}function pM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Pn(t,e))return;n.uniform4fv(this.addr,e),Ln(t,e)}}function mM(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Pn(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),Ln(t,e)}else{if(Pn(t,i))return;_0.set(i),n.uniformMatrix2fv(this.addr,!1,_0),Ln(t,i)}}function gM(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Pn(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),Ln(t,e)}else{if(Pn(t,i))return;g0.set(i),n.uniformMatrix3fv(this.addr,!1,g0),Ln(t,i)}}function _M(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Pn(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),Ln(t,e)}else{if(Pn(t,i))return;m0.set(i),n.uniformMatrix4fv(this.addr,!1,m0),Ln(t,i)}}function xM(n,e){let t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function vM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Pn(t,e))return;n.uniform2iv(this.addr,e),Ln(t,e)}}function yM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Pn(t,e))return;n.uniform3iv(this.addr,e),Ln(t,e)}}function MM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Pn(t,e))return;n.uniform4iv(this.addr,e),Ln(t,e)}}function EM(n,e){let t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function bM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Pn(t,e))return;n.uniform2uiv(this.addr,e),Ln(t,e)}}function TM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Pn(t,e))return;n.uniform3uiv(this.addr,e),Ln(t,e)}}function SM(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Pn(t,e))return;n.uniform4uiv(this.addr,e),Ln(t,e)}}function wM(n,e,t){let i=this.cache,s=t.allocateTextureUnit();i[0]!==s&&(n.uniform1i(this.addr,s),i[0]=s);let r;this.type===n.SAMPLER_2D_SHADOW?(of.compareFunction=t.isReversedDepthBuffer()?ru:su,r=of):r=L0,t.setTexture2D(e||r,s)}function AM(n,e,t){let i=this.cache,s=t.allocateTextureUnit();i[0]!==s&&(n.uniform1i(this.addr,s),i[0]=s),t.setTexture3D(e||N0,s)}function RM(n,e,t){let i=this.cache,s=t.allocateTextureUnit();i[0]!==s&&(n.uniform1i(this.addr,s),i[0]=s),t.setTextureCube(e||U0,s)}function CM(n,e,t){let i=this.cache,s=t.allocateTextureUnit();i[0]!==s&&(n.uniform1i(this.addr,s),i[0]=s),t.setTexture2DArray(e||D0,s)}function IM(n){switch(n){case 5126:return uM;case 35664:return dM;case 35665:return fM;case 35666:return pM;case 35674:return mM;case 35675:return gM;case 35676:return _M;case 5124:case 35670:return xM;case 35667:case 35671:return vM;case 35668:case 35672:return yM;case 35669:case 35673:return MM;case 5125:return EM;case 36294:return bM;case 36295:return TM;case 36296:return SM;case 35678:case 36198:case 36298:case 36306:case 35682:return wM;case 35679:case 36299:case 36307:return AM;case 35680:case 36300:case 36308:case 36293:return RM;case 36289:case 36303:case 36311:case 36292:return CM}}function PM(n,e){n.uniform1fv(this.addr,e)}function LM(n,e){let t=ma(e,this.size,2);n.uniform2fv(this.addr,t)}function DM(n,e){let t=ma(e,this.size,3);n.uniform3fv(this.addr,t)}function NM(n,e){let t=ma(e,this.size,4);n.uniform4fv(this.addr,t)}function UM(n,e){let t=ma(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function FM(n,e){let t=ma(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function OM(n,e){let t=ma(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function BM(n,e){n.uniform1iv(this.addr,e)}function HM(n,e){n.uniform2iv(this.addr,e)}function kM(n,e){n.uniform3iv(this.addr,e)}function VM(n,e){n.uniform4iv(this.addr,e)}function zM(n,e){n.uniform1uiv(this.addr,e)}function GM(n,e){n.uniform2uiv(this.addr,e)}function WM(n,e){n.uniform3uiv(this.addr,e)}function XM(n,e){n.uniform4uiv(this.addr,e)}function qM(n,e,t){let i=this.cache,s=e.length,r=du(t,s);Pn(i,r)||(n.uniform1iv(this.addr,r),Ln(i,r));let o;this.type===n.SAMPLER_2D_SHADOW?o=of:o=L0;for(let a=0;a!==s;++a)t.setTexture2D(e[a]||o,r[a])}function YM(n,e,t){let i=this.cache,s=e.length,r=du(t,s);Pn(i,r)||(n.uniform1iv(this.addr,r),Ln(i,r));for(let o=0;o!==s;++o)t.setTexture3D(e[o]||N0,r[o])}function $M(n,e,t){let i=this.cache,s=e.length,r=du(t,s);Pn(i,r)||(n.uniform1iv(this.addr,r),Ln(i,r));for(let o=0;o!==s;++o)t.setTextureCube(e[o]||U0,r[o])}function ZM(n,e,t){let i=this.cache,s=e.length,r=du(t,s);Pn(i,r)||(n.uniform1iv(this.addr,r),Ln(i,r));for(let o=0;o!==s;++o)t.setTexture2DArray(e[o]||D0,r[o])}function KM(n){switch(n){case 5126:return PM;case 35664:return LM;case 35665:return DM;case 35666:return NM;case 35674:return UM;case 35675:return FM;case 35676:return OM;case 5124:case 35670:return BM;case 35667:case 35671:return HM;case 35668:case 35672:return kM;case 35669:case 35673:return VM;case 5125:return zM;case 36294:return GM;case 36295:return WM;case 36296:return XM;case 35678:case 36198:case 36298:case 36306:case 35682:return qM;case 35679:case 36299:case 36307:return YM;case 35680:case 36300:case 36308:case 36293:return $M;case 36289:case 36303:case 36311:case 36292:return ZM}}var af=class{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=IM(t.type)}},lf=class{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=KM(t.type)}},cf=class{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){let s=this.seq;for(let r=0,o=s.length;r!==o;++r){let a=s[r];a.setValue(e,t[a.id],i)}}},sf=/(\w+)(\])?(\[|\.)?/g;function x0(n,e){n.seq.push(e),n.map[e.id]=e}function jM(n,e,t){let i=n.name,s=i.length;for(sf.lastIndex=0;;){let r=sf.exec(i),o=sf.lastIndex,a=r[1],c=r[2]==="]",l=r[3];if(c&&(a=a|0),l===void 0||l==="["&&o+2===s){x0(t,l===void 0?new af(a,n,e):new lf(a,n,e));break}else{let d=t.map[a];d===void 0&&(d=new cf(a),x0(t,d)),t=d}}}var fa=class{constructor(e,t){this.seq=[],this.map={};let i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let o=0;o<i;++o){let a=e.getActiveUniform(t,o),c=e.getUniformLocation(t,a.name);jM(a,c,this)}let s=[],r=[];for(let o of this.seq)o.type===e.SAMPLER_2D_SHADOW||o.type===e.SAMPLER_CUBE_SHADOW||o.type===e.SAMPLER_2D_ARRAY_SHADOW?s.push(o):r.push(o);s.length>0&&(this.seq=s.concat(r))}setValue(e,t,i,s){let r=this.map[t];r!==void 0&&r.setValue(e,i,s)}setOptional(e,t,i){let s=t[i];s!==void 0&&this.setValue(e,i,s)}static upload(e,t,i,s){for(let r=0,o=t.length;r!==o;++r){let a=t[r],c=i[a.id];c.needsUpdate!==!1&&a.setValue(e,c.value,s)}}static seqWithValue(e,t){let i=[];for(let s=0,r=e.length;s!==r;++s){let o=e[s];o.id in t&&i.push(o)}return i}};function v0(n,e,t){let i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}var JM=37297,QM=0;function eE(n,e){let t=n.split(`
`),i=[],s=Math.max(e-6,0),r=Math.min(e+6,t.length);for(let o=s;o<r;o++){let a=o+1;i.push(`${a===e?">":" "} ${a}: ${t[o]}`)}return i.join(`
`)}var y0=new gt;function tE(n){It._getMatrix(y0,It.workingColorSpace,n);let e=`mat3( ${y0.elements.map(t=>t.toFixed(4))} )`;switch(It.getTransfer(n)){case Ka:return[e,"LinearTransferOETF"];case Gt:return[e,"sRGBTransferOETF"];default:return nt("WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function M0(n,e,t){let i=n.getShaderParameter(e,n.COMPILE_STATUS),r=(n.getShaderInfoLog(e)||"").trim();if(i&&r==="")return"";let o=/ERROR: 0:(\d+)/.exec(r);if(o){let a=parseInt(o[1]);return t.toUpperCase()+`

`+r+`

`+eE(n.getShaderSource(e),a)}else return r}function nE(n,e){let t=tE(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}var iE={[Pd]:"Linear",[Ld]:"Reinhard",[Dd]:"Cineon",[Ml]:"ACESFilmic",[Ud]:"AgX",[Fd]:"Neutral",[Nd]:"Custom"};function sE(n,e){let t=iE[e];return t===void 0?(nt("WebGLProgram: Unsupported toneMapping:",e),"vec3 "+n+"( vec3 color ) { return LinearToneMapping( color ); }"):"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}var lu=new y;function rE(){It.getLuminanceCoefficients(lu);let n=lu.x.toFixed(4),e=lu.y.toFixed(4),t=lu.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function oE(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Ll).join(`
`)}function aE(n){let e=[];for(let t in n){let i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function lE(n,e){let t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let s=0;s<i;s++){let r=n.getActiveAttrib(e,s),o=r.name,a=1;r.type===n.FLOAT_MAT2&&(a=2),r.type===n.FLOAT_MAT3&&(a=3),r.type===n.FLOAT_MAT4&&(a=4),t[o]={type:r.type,location:n.getAttribLocation(e,o),locationSize:a}}return t}function Ll(n){return n!==""}function E0(n,e){let t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_SUN_LIGHTS/g,e.numSunLights).replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_SUN_LIGHT_SHADOWS/g,e.numSunLightShadows).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function b0(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}var cE=/^[ \t]*#include +<([\w\d./]+)>/gm;function hf(n){return n.replace(cE,uE)}var hE=new Map;function uE(n,e){let t=At[e];if(t===void 0){let i=hE.get(e);if(i!==void 0)t=At[i],nt('WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("THREE.WebGLProgram: Can not resolve #include <"+e+">")}return hf(t)}var dE=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function T0(n){return n.replace(dE,fE)}function fE(n,e,t,i){let s="";for(let r=parseInt(e);r<parseInt(t);r++)s+=i.replace(/\[\s*i\s*\]/g,"[ "+r+" ]").replace(/UNROLLED_LOOP_INDEX/g,r);return s}function S0(n){let e=`precision ${n.precision} float;
	precision ${n.precision} int;
	precision ${n.precision} sampler2D;
	precision ${n.precision} samplerCube;
	precision ${n.precision} sampler3D;
	precision ${n.precision} sampler2DArray;
	precision ${n.precision} sampler2DShadow;
	precision ${n.precision} samplerCubeShadow;
	precision ${n.precision} sampler2DArrayShadow;
	precision ${n.precision} isampler2D;
	precision ${n.precision} isampler3D;
	precision ${n.precision} isamplerCube;
	precision ${n.precision} isampler2DArray;
	precision ${n.precision} usampler2D;
	precision ${n.precision} usampler3D;
	precision ${n.precision} usamplerCube;
	precision ${n.precision} usampler2DArray;
	`;return n.precision==="highp"?e+=`
#define HIGH_PRECISION`:n.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:n.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}var pE={[yl]:"SHADOWMAP_TYPE_PCF",[ra]:"SHADOWMAP_TYPE_VSM"};function mE(n){return pE[n.shadowMapType]||"SHADOWMAP_TYPE_BASIC"}var gE={[gr]:"ENVMAP_TYPE_CUBE",[to]:"ENVMAP_TYPE_CUBE",[El]:"ENVMAP_TYPE_CUBE_UV"};function _E(n){return n.envMap===!1?"ENVMAP_TYPE_CUBE":gE[n.envMapMode]||"ENVMAP_TYPE_CUBE"}var xE={[to]:"ENVMAP_MODE_REFRACTION"};function vE(n){return n.envMap===!1?"ENVMAP_MODE_REFLECTION":xE[n.envMapMode]||"ENVMAP_MODE_REFLECTION"}var yE={[Id]:"ENVMAP_BLENDING_MULTIPLY",[zm]:"ENVMAP_BLENDING_MIX",[Gm]:"ENVMAP_BLENDING_ADD"};function ME(n){return n.envMap===!1?"ENVMAP_BLENDING_NONE":yE[n.combine]||"ENVMAP_BLENDING_NONE"}function EE(n){let e=n.envMapCubeUVHeight;if(e===null)return null;let t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function bE(n,e,t,i){let s=n.getContext(),r=t.defines,o=t.vertexShader,a=t.fragmentShader,c=mE(t),l=_E(t),u=vE(t),d=ME(t),f=EE(t),p=oE(t),x=aE(r),b=s.createProgram(),g,m,A=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(g=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,x].filter(Ll).join(`
`),g.length>0&&(g+=`
`),m=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,x].filter(Ll).join(`
`),m.length>0&&(m+=`
`)):(g=[S0(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,x,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+u:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexNormals?"#define HAS_NORMAL":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",t.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Ll).join(`
`),m=[S0(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,x,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+u:"",t.envMap?"#define "+d:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.packedNormalMap?"#define USE_PACKED_NORMALMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.retroreflection?"#define USE_RETROREFLECTION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor?"#define USE_COLOR":"",t.vertexAlphas||t.batchingColor?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.numLightProbeGrids>0?"#define USE_LIGHT_PROBES_GRID":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",t.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==ns?"#define TONE_MAPPING":"",t.toneMapping!==ns?At.tonemapping_pars_fragment:"",t.toneMapping!==ns?sE("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",At.colorspace_pars_fragment,nE("linearToOutputTexel",t.outputColorSpace),rE(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Ll).join(`
`)),o=hf(o),o=E0(o,t),o=b0(o,t),a=hf(a),a=E0(a,t),a=b0(a,t),o=T0(o),a=T0(a),t.isRawShaderMaterial!==!0&&(A=`#version 300 es
`,g=[p,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+g,m=["#define varying in",t.glslVersion===qd?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===qd?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+m);let U=A+g+o,T=A+m+a,I=v0(s,s.VERTEX_SHADER,U),L=v0(s,s.FRAGMENT_SHADER,T);s.attachShader(b,I),s.attachShader(b,L),t.index0AttributeName!==void 0?s.bindAttribLocation(b,0,t.index0AttributeName):t.hasPositionAttribute===!0&&s.bindAttribLocation(b,0,"position"),s.linkProgram(b);function P(H){if(n.debug.checkShaderErrors){let k=s.getProgramInfoLog(b)||"",q=s.getShaderInfoLog(I)||"",z=s.getShaderInfoLog(L)||"",ee=k.trim(),he=q.trim(),ue=z.trim(),ye=!0,V=!0;if(s.getProgramParameter(b,s.LINK_STATUS)===!1)if(ye=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(s,b,I,L);else{let Q=M0(s,I,"vertex"),le=M0(s,L,"fragment");ht("WebGLProgram: Shader Error "+s.getError()+" - VALIDATE_STATUS "+s.getProgramParameter(b,s.VALIDATE_STATUS)+`

Material Name: `+H.name+`
Material Type: `+H.type+`

Program Info Log: `+ee+`
`+Q+`
`+le)}else ee!==""?nt("WebGLProgram: Program Info Log:",ee):(he===""||ue==="")&&(V=!1);V&&(H.diagnostics={runnable:ye,programLog:ee,vertexShader:{log:he,prefix:g},fragmentShader:{log:ue,prefix:m}})}s.deleteShader(I),s.deleteShader(L),M=new fa(s,b),C=lE(s,b)}let M;this.getUniforms=function(){return M===void 0&&P(this),M};let C;this.getAttributes=function(){return C===void 0&&P(this),C};let O=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return O===!1&&(O=s.getProgramParameter(b,JM)),O},this.destroy=function(){i.releaseStatesOfProgram(this),s.deleteProgram(b),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=QM++,this.cacheKey=e,this.usedTimes=1,this.program=b,this.vertexShader=I,this.fragmentShader=L,this}var TE=0,uf=class{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e,t,i){let s=this._getShaderCacheForMaterial(e);return s.has(t)===!1&&(s.add(t),t.usedTimes++),s.has(i)===!1&&(s.add(i),i.usedTimes++),this}remove(e){let t=this.materialCache.get(e);for(let i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderStage(e){return this._getShaderStage(e.vertexShader)}getFragmentShaderStage(e){return this._getShaderStage(e.fragmentShader)}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){let t=this.materialCache,i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){let t=this.shaderCache,i=t.get(e);return i===void 0&&(i=new df(e),t.set(e,i)),i}},df=class{constructor(e){this.id=TE++,this.code=e,this.usedTimes=0}};function SE(n){return n===xr||n===Al||n===Rl}function wE(n,e,t,i,s,r){let o=new Zo,a=new uf,c=new Set,l=[],u=new Map,d=i.logarithmicDepthBuffer,f=i.precision,p={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distance",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function x(M){return c.add(M),M===0?"uv":`uv${M}`}function b(M,C,O,H,k,q){let z=H.fog,ee=k.geometry,he=M.isMeshStandardMaterial||M.isMeshLambertMaterial||M.isMeshPhongMaterial?H.environment:null,ue=M.isMeshStandardMaterial||M.isMeshLambertMaterial&&!M.envMap||M.isMeshPhongMaterial&&!M.envMap,ye=e.get(M.envMap||he,ue),V=ye&&ye.mapping===El?ye.image.height:null,Q=p[M.type];M.precision!==null&&(f=i.getMaxPrecision(M.precision),f!==M.precision&&nt("WebGLProgram.getParameters:",M.precision,"not supported, using",f,"instead."));let le=ee.morphAttributes.position||ee.morphAttributes.normal||ee.morphAttributes.color,Ee=le!==void 0?le.length:0,be=0;ee.morphAttributes.position!==void 0&&(be=1),ee.morphAttributes.normal!==void 0&&(be=2),ee.morphAttributes.color!==void 0&&(be=3);let ut,et,ct,ae;if(Q){let Xt=Ss[Q];ut=Xt.vertexShader,et=Xt.fragmentShader}else{ut=M.vertexShader,et=M.fragmentShader;let Xt=a.getVertexShaderStage(M),De=a.getFragmentShaderStage(M);a.update(M,Xt,De),ct=Xt.id,ae=De.id}let me=n.getRenderTarget(),qe=n.state.buffers.depth.getReversed(),ft=k.isInstancedMesh===!0,Ge=k.isBatchedMesh===!0,Et=!!M.map,pn=!!M.matcap,bt=!!ye,Ft=!!M.aoMap,Wt=!!M.lightMap,Tt=!!M.bumpMap&&M.wireframe===!1,Jt=!!M.normalMap,bn=!!M.displacementMap,xe=!!M.emissiveMap,vt=!!M.metalnessMap,Rt=!!M.roughnessMap,X=M.anisotropy>0,xn=M.clearcoat>0,lt=M.dispersion>0,B=M.retroreflectivity>0,E=M.iridescence>0,$=M.sheen>0,se=M.transmission>0,de=X&&!!M.anisotropyMap,we=xn&&!!M.clearcoatMap,Ae=xn&&!!M.clearcoatNormalMap,ce=xn&&!!M.clearcoatRoughnessMap,re=E&&!!M.iridescenceMap,Ie=E&&!!M.iridescenceThicknessMap,Ze=$&&!!M.sheenColorMap,Fe=$&&!!M.sheenRoughnessMap,Se=!!M.specularMap,it=!!M.specularColorMap,ot=!!M.specularIntensityMap,xt=se&&!!M.transmissionMap,W=se&&!!M.thicknessMap,Te=!!M.gradientMap,oe=!!M.alphaMap,Re=M.alphaTest>0,He=!!M.alphaHash,ve=!!M.extensions,st=ns;M.toneMapped&&(me===null||me.isXRRenderTarget===!0)&&(st=n.toneMapping);let Je={shaderID:Q,shaderType:M.type,shaderName:M.name,vertexShader:ut,fragmentShader:et,defines:M.defines,customVertexShaderID:ct,customFragmentShaderID:ae,isRawShaderMaterial:M.isRawShaderMaterial===!0,glslVersion:M.glslVersion,precision:f,batching:Ge,batchingColor:Ge&&k._colorsTexture!==null,instancing:ft,instancingColor:ft&&k.instanceColor!==null,instancingMorph:ft&&k.morphTexture!==null,outputColorSpace:me===null?n.outputColorSpace:me.isXRRenderTarget===!0?me.texture.colorSpace:It.workingColorSpace,alphaToCoverage:!!M.alphaToCoverage,map:Et,matcap:pn,envMap:bt,envMapMode:bt&&ye.mapping,envMapCubeUVHeight:V,aoMap:Ft,lightMap:Wt,bumpMap:Tt,normalMap:Jt,displacementMap:bn,emissiveMap:xe,normalMapObjectSpace:Jt&&M.normalMapType===Ym,normalMapTangentSpace:Jt&&M.normalMapType===iu,packedNormalMap:Jt&&M.normalMapType===iu&&SE(M.normalMap.format),metalnessMap:vt,roughnessMap:Rt,anisotropy:X,anisotropyMap:de,clearcoat:xn,clearcoatMap:we,clearcoatNormalMap:Ae,clearcoatRoughnessMap:ce,dispersion:lt,retroreflection:B,iridescence:E,iridescenceMap:re,iridescenceThicknessMap:Ie,sheen:$,sheenColorMap:Ze,sheenRoughnessMap:Fe,specularMap:Se,specularColorMap:it,specularIntensityMap:ot,transmission:se,transmissionMap:xt,thicknessMap:W,gradientMap:Te,opaque:M.transparent===!1&&M.blending===Ui&&M.alphaToCoverage===!1,alphaMap:oe,alphaTest:Re,alphaHash:He,combine:M.combine,mapUv:Et&&x(M.map.channel),aoMapUv:Ft&&x(M.aoMap.channel),lightMapUv:Wt&&x(M.lightMap.channel),bumpMapUv:Tt&&x(M.bumpMap.channel),normalMapUv:Jt&&x(M.normalMap.channel),displacementMapUv:bn&&x(M.displacementMap.channel),emissiveMapUv:xe&&x(M.emissiveMap.channel),metalnessMapUv:vt&&x(M.metalnessMap.channel),roughnessMapUv:Rt&&x(M.roughnessMap.channel),anisotropyMapUv:de&&x(M.anisotropyMap.channel),clearcoatMapUv:we&&x(M.clearcoatMap.channel),clearcoatNormalMapUv:Ae&&x(M.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:ce&&x(M.clearcoatRoughnessMap.channel),iridescenceMapUv:re&&x(M.iridescenceMap.channel),iridescenceThicknessMapUv:Ie&&x(M.iridescenceThicknessMap.channel),sheenColorMapUv:Ze&&x(M.sheenColorMap.channel),sheenRoughnessMapUv:Fe&&x(M.sheenRoughnessMap.channel),specularMapUv:Se&&x(M.specularMap.channel),specularColorMapUv:it&&x(M.specularColorMap.channel),specularIntensityMapUv:ot&&x(M.specularIntensityMap.channel),transmissionMapUv:xt&&x(M.transmissionMap.channel),thicknessMapUv:W&&x(M.thicknessMap.channel),alphaMapUv:oe&&x(M.alphaMap.channel),vertexTangents:!!ee.attributes.tangent&&(Jt||X),vertexNormals:!!ee.attributes.normal,vertexColors:M.vertexColors,vertexAlphas:M.vertexColors===!0&&!!ee.attributes.color&&ee.attributes.color.itemSize===4,pointsUvs:k.isPoints===!0&&!!ee.attributes.uv&&(Et||oe),fog:!!z,useFog:M.fog===!0,fogExp2:!!z&&z.isFogExp2,flatShading:M.wireframe===!1&&(M.flatShading===!0||ee.attributes.normal===void 0&&Jt===!1&&(M.isMeshLambertMaterial||M.isMeshPhongMaterial||M.isMeshStandardMaterial||M.isMeshPhysicalMaterial)),sizeAttenuation:M.sizeAttenuation===!0,logarithmicDepthBuffer:d,reversedDepthBuffer:qe,skinning:k.isSkinnedMesh===!0,hasPositionAttribute:ee.attributes.position!==void 0,morphTargets:ee.morphAttributes.position!==void 0,morphNormals:ee.morphAttributes.normal!==void 0,morphColors:ee.morphAttributes.color!==void 0,morphTargetsCount:Ee,morphTextureStride:be,numSunLights:C.sun.length,numDirLights:C.directional.length,numPointLights:C.point.length,numSpotLights:C.spot.length,numSpotLightMaps:C.spotLightMap.length,numRectAreaLights:C.rectArea.length,numHemiLights:C.hemi.length,numSunLightShadows:C.sunShadowMap.length,numDirLightShadows:C.directionalShadowMap.length,numPointLightShadows:C.pointShadowMap.length,numSpotLightShadows:C.spotShadowMap.length,numSpotLightShadowsWithMaps:C.numSpotLightShadowsWithMaps,numLightProbes:C.numLightProbes,numLightProbeGrids:q.length,numClippingPlanes:r.numPlanes,numClipIntersection:r.numIntersection,dithering:M.dithering,shadowMapEnabled:n.shadowMap.enabled&&O.length>0,shadowMapType:n.shadowMap.type,toneMapping:st,decodeVideoTexture:Et&&M.map.isVideoTexture===!0&&It.getTransfer(M.map.colorSpace)===Gt,decodeVideoTextureEmissive:xe&&M.emissiveMap.isVideoTexture===!0&&It.getTransfer(M.emissiveMap.colorSpace)===Gt,premultipliedAlpha:M.premultipliedAlpha,doubleSided:M.side===mn,flipSided:M.side===Hn,useDepthPacking:M.depthPacking>=0,depthPacking:M.depthPacking||0,index0AttributeName:M.index0AttributeName,extensionClipCullDistance:ve&&M.extensions.clipCullDistance===!0&&t.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(ve&&M.extensions.multiDraw===!0||Ge)&&t.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:t.has("KHR_parallel_shader_compile"),customProgramCacheKey:M.customProgramCacheKey()};return Je.vertexUv1s=c.has(1),Je.vertexUv2s=c.has(2),Je.vertexUv3s=c.has(3),c.clear(),Je}function g(M){let C=[];if(M.shaderID?C.push(M.shaderID):(C.push(M.customVertexShaderID),C.push(M.customFragmentShaderID)),M.defines!==void 0)for(let O in M.defines)C.push(O),C.push(M.defines[O]);return M.isRawShaderMaterial===!1&&(m(C,M),A(C,M),C.push(n.outputColorSpace)),C.push(M.customProgramCacheKey),C.join()}function m(M,C){M.push(C.precision),M.push(C.outputColorSpace),M.push(C.envMapMode),M.push(C.envMapCubeUVHeight),M.push(C.mapUv),M.push(C.alphaMapUv),M.push(C.lightMapUv),M.push(C.aoMapUv),M.push(C.bumpMapUv),M.push(C.normalMapUv),M.push(C.displacementMapUv),M.push(C.emissiveMapUv),M.push(C.metalnessMapUv),M.push(C.roughnessMapUv),M.push(C.anisotropyMapUv),M.push(C.clearcoatMapUv),M.push(C.clearcoatNormalMapUv),M.push(C.clearcoatRoughnessMapUv),M.push(C.iridescenceMapUv),M.push(C.iridescenceThicknessMapUv),M.push(C.sheenColorMapUv),M.push(C.sheenRoughnessMapUv),M.push(C.specularMapUv),M.push(C.specularColorMapUv),M.push(C.specularIntensityMapUv),M.push(C.transmissionMapUv),M.push(C.thicknessMapUv),M.push(C.combine),M.push(C.fogExp2),M.push(C.sizeAttenuation),M.push(C.morphTargetsCount),M.push(C.morphAttributeCount),M.push(C.numSunLights),M.push(C.numDirLights),M.push(C.numPointLights),M.push(C.numSpotLights),M.push(C.numSpotLightMaps),M.push(C.numHemiLights),M.push(C.numRectAreaLights),M.push(C.numSunLightShadows),M.push(C.numDirLightShadows),M.push(C.numPointLightShadows),M.push(C.numSpotLightShadows),M.push(C.numSpotLightShadowsWithMaps),M.push(C.numLightProbes),M.push(C.shadowMapType),M.push(C.toneMapping),M.push(C.numClippingPlanes),M.push(C.numClipIntersection),M.push(C.depthPacking)}function A(M,C){o.disableAll(),C.instancing&&o.enable(0),C.instancingColor&&o.enable(1),C.instancingMorph&&o.enable(2),C.matcap&&o.enable(3),C.envMap&&o.enable(4),C.normalMapObjectSpace&&o.enable(5),C.normalMapTangentSpace&&o.enable(6),C.clearcoat&&o.enable(7),C.iridescence&&o.enable(8),C.alphaTest&&o.enable(9),C.vertexColors&&o.enable(10),C.vertexAlphas&&o.enable(11),C.vertexUv1s&&o.enable(12),C.vertexUv2s&&o.enable(13),C.vertexUv3s&&o.enable(14),C.vertexTangents&&o.enable(15),C.anisotropy&&o.enable(16),C.alphaHash&&o.enable(17),C.batching&&o.enable(18),C.dispersion&&o.enable(19),C.retroreflection&&o.enable(24),C.batchingColor&&o.enable(20),C.gradientMap&&o.enable(21),C.packedNormalMap&&o.enable(22),C.vertexNormals&&o.enable(23),M.push(o.mask),o.disableAll(),C.fog&&o.enable(0),C.useFog&&o.enable(1),C.flatShading&&o.enable(2),C.logarithmicDepthBuffer&&o.enable(3),C.reversedDepthBuffer&&o.enable(4),C.skinning&&o.enable(5),C.morphTargets&&o.enable(6),C.morphNormals&&o.enable(7),C.morphColors&&o.enable(8),C.premultipliedAlpha&&o.enable(9),C.shadowMapEnabled&&o.enable(10),C.doubleSided&&o.enable(11),C.flipSided&&o.enable(12),C.useDepthPacking&&o.enable(13),C.dithering&&o.enable(14),C.transmission&&o.enable(15),C.sheen&&o.enable(16),C.opaque&&o.enable(17),C.pointsUvs&&o.enable(18),C.decodeVideoTexture&&o.enable(19),C.decodeVideoTextureEmissive&&o.enable(20),C.alphaToCoverage&&o.enable(21),C.numLightProbeGrids>0&&o.enable(22),C.hasPositionAttribute&&o.enable(23),M.push(o.mask)}function U(M){let C=p[M.type],O;if(C){let H=Ss[C];O=ou.clone(H.uniforms)}else O=M.uniforms;return O}function T(M,C){let O=u.get(C);return O!==void 0?++O.usedTimes:(O=new bE(n,C,M,s),l.push(O),u.set(C,O)),O}function I(M){if(--M.usedTimes===0){let C=l.indexOf(M);l[C]=l[l.length-1],l.pop(),u.delete(M.cacheKey),M.destroy()}}function L(M){a.remove(M)}function P(){a.dispose()}return{getParameters:b,getProgramCacheKey:g,getUniforms:U,acquireProgram:T,releaseProgram:I,releaseShaderCache:L,programs:l,dispose:P}}function AE(){let n=new WeakMap;function e(o){return n.has(o)}function t(o){let a=n.get(o);return a===void 0&&(a={},n.set(o,a)),a}function i(o){n.delete(o)}function s(o,a,c){n.get(o)[a]=c}function r(){n=new WeakMap}return{has:e,get:t,remove:i,update:s,dispose:r}}function RE(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.materialVariant!==e.materialVariant?n.materialVariant-e.materialVariant:n.z!==e.z?n.z-e.z:n.id-e.id}function w0(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function A0(){let n=[],e=0,t=[],i=[],s=[];function r(){e=0,t.length=0,i.length=0,s.length=0}function o(f){let p=0;return f.isInstancedMesh&&(p+=2),f.isSkinnedMesh&&(p+=1),p}function a(f,p,x,b,g,m){let A=n[e];return A===void 0?(A={id:f.id,object:f,geometry:p,material:x,materialVariant:o(f),groupOrder:b,renderOrder:f.renderOrder,z:g,group:m},n[e]=A):(A.id=f.id,A.object=f,A.geometry=p,A.material=x,A.materialVariant=o(f),A.groupOrder=b,A.renderOrder=f.renderOrder,A.z=g,A.group=m),e++,A}function c(f,p,x,b,g,m,A){A.reversedDepth===!0&&(g=-g);let U=a(f,p,x,b,g,m);x.transmission>0?i.push(U):x.transparent===!0?s.push(U):t.push(U)}function l(f,p,x,b,g,m){let A=a(f,p,x,b,g,m);x.transmission>0?i.unshift(A):x.transparent===!0?s.unshift(A):t.unshift(A)}function u(f,p){t.length>1&&t.sort(f||RE),i.length>1&&i.sort(p||w0),s.length>1&&s.sort(p||w0)}function d(){for(let f=e,p=n.length;f<p;f++){let x=n[f];if(x.id===null)break;x.id=null,x.object=null,x.geometry=null,x.material=null,x.group=null}}return{opaque:t,transmissive:i,transparent:s,init:r,push:c,unshift:l,finish:d,sort:u}}function CE(){let n=new WeakMap;function e(i,s){let r=n.get(i),o;return r===void 0?(o=new A0,n.set(i,[o])):s>=r.length?(o=new A0,r.push(o)):o=r[s],o}function t(){n=new WeakMap}return{get:e,dispose:t}}function IE(){let n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"SunLight":case"DirectionalLight":t={direction:new y,color:new ke};break;case"SpotLight":t={position:new y,direction:new y,color:new ke,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new y,color:new ke,distance:0,decay:0};break;case"HemisphereLight":t={direction:new y,skyColor:new ke,groundColor:new ke};break;case"RectAreaLight":t={color:new ke,position:new y,halfWidth:new y,halfHeight:new y};break}return n[e.id]=t,t}}}function PE(){let n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"SunLight":case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Pe};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Pe};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Pe,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}var LE=0;function DE(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function NE(n){let e=new IE,t=PE(),i={version:0,hash:{sunLength:-1,directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numSunShadows:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],sun:[],sunShadow:[],sunShadowMap:[],sunShadowMatrix:[],sunShadowCascade:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new y);let s=new y,r=new rt,o=new rt;function a(l){let u=0,d=0,f=0;for(let k=0;k<9;k++)i.probe[k].set(0,0,0);let p=0,x=0,b=0,g=0,m=0,A=0,U=0,T=0,I=0,L=0,P=0,M=0,C=0,O=0;l.sort(DE);for(let k=0,q=l.length;k<q;k++){let z=l[k],ee=z.color,he=z.intensity,ue=z.distance,ye=null;if(z.shadow&&z.shadow.map&&(z.shadow.map.texture.format===xr?ye=z.shadow.map.texture:ye=z.shadow.map.depthTexture||z.shadow.map.texture),z.isAmbientLight)u+=ee.r*he,d+=ee.g*he,f+=ee.b*he;else if(z.isLightProbe){for(let V=0;V<9;V++)i.probe[V].addScaledVector(z.sh.coefficients[V],he);O++}else if(z.isSunLight){let V=e.get(z);if(V.color.copy(z.color).multiplyScalar(z.intensity),z.castShadow){let Q=z.shadow,le=t.get(z);le.shadowIntensity=Q.intensity,le.shadowBias=Q.bias,le.shadowNormalBias=Q.normalBias,le.shadowRadius=Q.radius,le.shadowMapSize.copy(Q.mapSize).multiply(Q.getFrameExtents()),i.sunShadow[x]=le,i.sunShadowMap[x]=ye;let Ee=Q.getViewportCount();for(let be=0;be<Ee;be++)i.sunShadowMatrix[b+be]=Q.getMatrix(be),i.sunShadowCascade[b+be]=Q._cascadeData[be];b+=Ee,x++}i.sun[p]=V,p++}else if(z.isDirectionalLight){let V=e.get(z);if(V.color.copy(z.color).multiplyScalar(z.intensity),z.castShadow){let Q=z.shadow,le=t.get(z);le.shadowIntensity=Q.intensity,le.shadowBias=Q.bias,le.shadowNormalBias=Q.normalBias,le.shadowRadius=Q.radius,le.shadowMapSize=Q.mapSize,i.directionalShadow[g]=le,i.directionalShadowMap[g]=ye,i.directionalShadowMatrix[g]=z.shadow.matrix,I++}i.directional[g]=V,g++}else if(z.isSpotLight){let V=e.get(z);V.position.setFromMatrixPosition(z.matrixWorld),V.color.copy(ee).multiplyScalar(he),V.distance=ue,V.coneCos=Math.cos(z.angle),V.penumbraCos=Math.cos(z.angle*(1-z.penumbra)),V.decay=z.decay,i.spot[A]=V;let Q=z.shadow;if(z.map&&(i.spotLightMap[M]=z.map,M++,Q.updateMatrices(z),z.castShadow&&C++),i.spotLightMatrix[A]=Q.matrix,z.castShadow){let le=t.get(z);le.shadowIntensity=Q.intensity,le.shadowBias=Q.bias,le.shadowNormalBias=Q.normalBias,le.shadowRadius=Q.radius,le.shadowMapSize=Q.mapSize,i.spotShadow[A]=le,i.spotShadowMap[A]=ye,P++}A++}else if(z.isRectAreaLight){let V=e.get(z);V.color.copy(ee).multiplyScalar(he),V.halfWidth.set(z.width*.5,0,0),V.halfHeight.set(0,z.height*.5,0),i.rectArea[U]=V,U++}else if(z.isPointLight){let V=e.get(z);if(V.color.copy(z.color).multiplyScalar(z.intensity),V.distance=z.distance,V.decay=z.decay,z.castShadow){let Q=z.shadow,le=t.get(z);le.shadowIntensity=Q.intensity,le.shadowBias=Q.bias,le.shadowNormalBias=Q.normalBias,le.shadowRadius=Q.radius,le.shadowMapSize=Q.mapSize,le.shadowCameraNear=Q.camera.near,le.shadowCameraFar=Q.camera.far,i.pointShadow[m]=le,i.pointShadowMap[m]=ye,i.pointShadowMatrix[m]=z.shadow.matrix,L++}i.point[m]=V,m++}else if(z.isHemisphereLight){let V=e.get(z);V.skyColor.copy(z.color).multiplyScalar(he),V.groundColor.copy(z.groundColor).multiplyScalar(he),i.hemi[T]=V,T++}}U>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=Be.LTC_FLOAT_1,i.rectAreaLTC2=Be.LTC_FLOAT_2):(i.rectAreaLTC1=Be.LTC_HALF_1,i.rectAreaLTC2=Be.LTC_HALF_2)),i.ambient[0]=u,i.ambient[1]=d,i.ambient[2]=f;let H=i.hash;(H.sunLength!==p||H.directionalLength!==g||H.pointLength!==m||H.spotLength!==A||H.rectAreaLength!==U||H.hemiLength!==T||H.numSunShadows!==x||H.numDirectionalShadows!==I||H.numPointShadows!==L||H.numSpotShadows!==P||H.numSpotMaps!==M||H.numLightProbes!==O)&&(i.sun.length=p,i.directional.length=g,i.spot.length=A,i.rectArea.length=U,i.point.length=m,i.hemi.length=T,i.sunShadow.length=x,i.sunShadowMap.length=x,i.sunShadowMatrix.length=b,i.sunShadowCascade.length=b,i.directionalShadow.length=I,i.directionalShadowMap.length=I,i.directionalShadowMatrix.length=I,i.pointShadow.length=L,i.pointShadowMap.length=L,i.pointShadowMatrix.length=L,i.spotShadow.length=P,i.spotShadowMap.length=P,i.spotLightMatrix.length=P+M-C,i.spotLightMap.length=M,i.numSpotLightShadowsWithMaps=C,i.numLightProbes=O,H.sunLength=p,H.directionalLength=g,H.pointLength=m,H.spotLength=A,H.rectAreaLength=U,H.hemiLength=T,H.numSunShadows=x,H.numDirectionalShadows=I,H.numPointShadows=L,H.numSpotShadows=P,H.numSpotMaps=M,H.numLightProbes=O,i.version=LE++)}function c(l,u){let d=0,f=0,p=0,x=0,b=0,g=0,m=u.matrixWorldInverse;for(let A=0,U=l.length;A<U;A++){let T=l[A];if(T.isSunLight){let I=i.sun[d];I.direction.setFromMatrixPosition(T.matrixWorld),I.direction.transformDirection(m),d++}else if(T.isDirectionalLight){let I=i.directional[f];I.direction.setFromMatrixPosition(T.matrixWorld),s.setFromMatrixPosition(T.target.matrixWorld),I.direction.sub(s),I.direction.transformDirection(m),f++}else if(T.isSpotLight){let I=i.spot[x];I.position.setFromMatrixPosition(T.matrixWorld),I.position.applyMatrix4(m),I.direction.setFromMatrixPosition(T.matrixWorld),s.setFromMatrixPosition(T.target.matrixWorld),I.direction.sub(s),I.direction.transformDirection(m),x++}else if(T.isRectAreaLight){let I=i.rectArea[b];I.position.setFromMatrixPosition(T.matrixWorld),I.position.applyMatrix4(m),o.identity(),r.copy(T.matrixWorld),r.premultiply(m),o.extractRotation(r),I.halfWidth.set(T.width*.5,0,0),I.halfHeight.set(0,T.height*.5,0),I.halfWidth.applyMatrix4(o),I.halfHeight.applyMatrix4(o),b++}else if(T.isPointLight){let I=i.point[p];I.position.setFromMatrixPosition(T.matrixWorld),I.position.applyMatrix4(m),p++}else if(T.isHemisphereLight){let I=i.hemi[g];I.direction.setFromMatrixPosition(T.matrixWorld),I.direction.transformDirection(m),g++}}}return{setup:a,setupView:c,state:i}}function R0(n){let e=new NE(n),t=[],i=[],s=[];function r(f){d.camera=f,t.length=0,i.length=0,s.length=0}function o(f){t.push(f)}function a(f){i.push(f)}function c(f){s.push(f)}function l(){e.setup(t)}function u(f){e.setupView(t,f)}let d={lightsArray:t,shadowsArray:i,lightProbeGridArray:s,camera:null,lights:e,transmissionRenderTarget:{},textureUnits:0};return{init:r,state:d,setupLights:l,setupLightsView:u,pushLight:o,pushShadow:a,pushLightProbeGrid:c}}function UE(n){let e=new WeakMap;function t(s,r=0){let o=e.get(s),a;return o===void 0?(a=new R0(n),e.set(s,[a])):r>=o.length?(a=new R0(n),o.push(a)):a=o[r],a}function i(){e=new WeakMap}return{get:t,dispose:i}}var FE=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,OE=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ).rg;
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ).r;
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( max( 0.0, squared_mean - mean * mean ) );
	gl_FragColor = vec4( mean, std_dev, 0.0, 1.0 );
}`,BE=[new y(1,0,0),new y(-1,0,0),new y(0,1,0),new y(0,-1,0),new y(0,0,1),new y(0,0,-1)],HE=[new y(0,-1,0),new y(0,-1,0),new y(0,0,1),new y(0,0,-1),new y(0,-1,0),new y(0,-1,0)],C0=new rt,Pl=new y,rf=new y;function kE(n,e,t){let i=new ea,s=new Pe,r=new Pe,o=new $t,a=new rh,c=new oh,l={},u=t.maxTextureSize,d={[Es]:Hn,[Hn]:Es,[mn]:mn},f=new Un({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Pe},radius:{value:4}},vertexShader:FE,fragmentShader:OE}),p=f.clone();p.defines.HORIZONTAL_PASS=1;let x=new tn;x.setAttribute("position",new Cn(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));let b=new dn(x,f),g=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=yl;let m=this.type;this.render=function(L,P,M){if(g.enabled===!1||g.autoUpdate===!1&&g.needsUpdate===!1||L.length===0)return;this.type===gh&&(nt("WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead."),this.type=yl);let C=n.getRenderTarget(),O=n.getActiveCubeFace(),H=n.getActiveMipmapLevel(),k=n.state;k.setBlending(bs),k.buffers.depth.getReversed()===!0?k.buffers.color.setClear(0,0,0,0):k.buffers.color.setClear(1,1,1,1),k.buffers.depth.setTest(!0),k.setScissorTest(!1);let q=m!==this.type;q&&P.traverse(function(z){z.material&&(Array.isArray(z.material)?z.material.forEach(ee=>ee.needsUpdate=!0):z.material.needsUpdate=!0)});for(let z=0,ee=L.length;z<ee;z++){let he=L[z],ue=he.shadow;if(ue===void 0){nt("WebGLShadowMap:",he,"has no shadow.");continue}if(ue.autoUpdate===!1&&ue.needsUpdate===!1)continue;s.copy(ue.mapSize);let ye=ue.getFrameExtents();s.multiply(ye),r.copy(ue.mapSize),(s.x>u||s.y>u)&&(s.x>u&&(r.x=Math.floor(u/ye.x),s.x=r.x*ye.x,ue.mapSize.x=r.x),s.y>u&&(r.y=Math.floor(u/ye.y),s.y=r.y*ye.y,ue.mapSize.y=r.y));let V=n.state.buffers.depth.getReversed();if(ue.camera._reversedDepth=V,ue.map===null||q===!0){if(ue.map!==null&&(ue.map.depthTexture!==null&&(ue.map.depthTexture.dispose(),ue.map.depthTexture=null),ue.map.dispose()),this.type===ra){if(he.isPointLight){nt("WebGLShadowMap: VSM shadow maps are not supported for PointLights. Use PCF or BasicShadowMap instead.");continue}ue.map=new ai(s.x,s.y,{format:xr,type:rs,minFilter:yn,magFilter:yn,generateMipmaps:!1}),ue.map.texture.name=he.name+".shadowMap",ue.map.depthTexture=new dr(s.x,s.y,Ti),ue.map.depthTexture.name=he.name+".shadowMapDepth",ue.map.depthTexture.format=xs,ue.map.depthTexture.compareFunction=null,ue.map.depthTexture.minFilter=vn,ue.map.depthTexture.magFilter=vn}else he.isPointLight?(ue.map=new cu(s.x),ue.map.depthTexture=new Kc(s.x,ss)):(ue.map=new ai(s.x,s.y),ue.map.depthTexture=new dr(s.x,s.y,ss)),ue.map.depthTexture.name=he.name+".shadowMap",ue.map.depthTexture.format=xs,this.type===yl?(ue.map.depthTexture.compareFunction=V?ru:su,ue.map.depthTexture.minFilter=yn,ue.map.depthTexture.magFilter=yn):(ue.map.depthTexture.compareFunction=null,ue.map.depthTexture.minFilter=vn,ue.map.depthTexture.magFilter=vn);ue.camera.updateProjectionMatrix()}ue.map.isWebGLCubeRenderTarget!==!0&&(ue.map.width!==s.x||ue.map.height!==s.y)&&ue.map.setSize(s.x,s.y);let Q=ue.map.isWebGLCubeRenderTarget?6:ue.getViewportCount();he.isPointLight!==!0&&ue.updateMatrices(he,M);for(let le=0;le<Q;le++){let Ee=ue.getCamera(le);if(he.isPointLight){let be=ue.camera,ut=ue.matrix,et=he.distance||be.far;et!==be.far&&(be.far=et,be.updateProjectionMatrix()),Pl.setFromMatrixPosition(he.matrixWorld),be.position.copy(Pl),rf.copy(be.position),rf.add(BE[le]),be.up.copy(HE[le]),be.lookAt(rf),be.updateMatrixWorld(),ut.makeTranslation(-Pl.x,-Pl.y,-Pl.z),C0.multiplyMatrices(be.projectionMatrix,be.matrixWorldInverse),ue._frustum.setFromProjectionMatrix(C0,be.coordinateSystem,be.reversedDepth)}if(ue.map.isWebGLCubeRenderTarget)n.setRenderTarget(ue.map,le),n.clear();else{le===0&&(n.setRenderTarget(ue.map),n.clear());let be=ue.getViewport(le);o.set(r.x*be.x,r.y*be.y,r.x*be.z,r.y*be.w),k.viewport(o)}i=ue.getFrustum(le),T(P,M,Ee,he,this.type)}ue.isPointLightShadow!==!0&&this.type===ra&&A(ue,M),ue.needsUpdate=!1}m=this.type,g.needsUpdate=!1,n.setRenderTarget(C,O,H)};function A(L,P){let M=e.update(b);f.defines.VSM_SAMPLES!==L.blurSamples&&(f.defines.VSM_SAMPLES=L.blurSamples,p.defines.VSM_SAMPLES=L.blurSamples,f.needsUpdate=!0,p.needsUpdate=!0),L.mapPass===null?L.mapPass=new ai(s.x,s.y,{format:xr,type:rs}):(L.mapPass.width!==L.map.width||L.mapPass.height!==L.map.height)&&L.mapPass.setSize(L.map.width,L.map.height),f.uniforms.shadow_pass.value=L.map.depthTexture,f.uniforms.resolution.value.set(L.map.width,L.map.height),f.uniforms.radius.value=L.radius,n.setRenderTarget(L.mapPass),n.clear(),n.renderBufferDirect(P,null,M,f,b,null),p.uniforms.shadow_pass.value=L.mapPass.texture,p.uniforms.resolution.value.set(L.map.width,L.map.height),p.uniforms.radius.value=L.radius,n.setRenderTarget(L.map),n.clear(),n.renderBufferDirect(P,null,M,p,b,null)}function U(L,P,M,C){let O=null,H=M.isPointLight===!0?L.customDistanceMaterial:L.customDepthMaterial;if(H!==void 0)O=H;else if(O=M.isPointLight===!0?c:a,n.localClippingEnabled&&P.clipShadows===!0&&Array.isArray(P.clippingPlanes)&&P.clippingPlanes.length!==0||P.displacementMap&&P.displacementScale!==0||P.alphaMap&&P.alphaTest>0||P.map&&P.alphaTest>0||P.alphaToCoverage===!0){let k=O.uuid,q=P.uuid,z=l[k];z===void 0&&(z={},l[k]=z);let ee=z[q];ee===void 0&&(ee=O.clone(),z[q]=ee,P.addEventListener("dispose",I)),O=ee}if(O.visible=P.visible,O.wireframe=P.wireframe,C===ra?O.side=P.shadowSide!==null?P.shadowSide:P.side:O.side=P.shadowSide!==null?P.shadowSide:d[P.side],O.alphaMap=P.alphaMap,O.alphaTest=P.alphaToCoverage===!0?.5:P.alphaTest,O.map=P.map,O.clipShadows=P.clipShadows,O.clippingPlanes=P.clippingPlanes,O.clipIntersection=P.clipIntersection,O.displacementMap=P.displacementMap,O.displacementScale=P.displacementScale,O.displacementBias=P.displacementBias,O.wireframeLinewidth=P.wireframeLinewidth,O.linewidth=P.linewidth,M.isPointLight===!0&&O.isMeshDistanceMaterial===!0){let k=n.properties.get(O);k.light=M}return O}function T(L,P,M,C,O){if(L.visible===!1)return;if(L.layers.test(P.layers)&&(L.isMesh||L.isLine||L.isPoints)&&(L.castShadow||L.receiveShadow&&O===ra)&&(!L.frustumCulled||L.intersectsFrustum(i))){L.modelViewMatrix.multiplyMatrices(M.matrixWorldInverse,L.matrixWorld);let q=e.update(L),z=L.material;if(Array.isArray(z)){let ee=q.groups;for(let he=0,ue=ee.length;he<ue;he++){let ye=ee[he],V=z[ye.materialIndex];if(V&&V.visible){let Q=U(L,V,C,O);L.onBeforeShadow(n,L,P,M,q,Q,ye),n.renderBufferDirect(M,null,q,Q,L,ye),L.onAfterShadow(n,L,P,M,q,Q,ye)}}}else if(z.visible){let ee=U(L,z,C,O);L.onBeforeShadow(n,L,P,M,q,ee,null),n.renderBufferDirect(M,null,q,ee,L,null),L.onAfterShadow(n,L,P,M,q,ee,null)}}let k=L.children;for(let q=0,z=k.length;q<z;q++)T(k[q],P,M,C,O)}function I(L){L.target.removeEventListener("dispose",I);for(let M in l){let C=l[M],O=L.target.uuid;O in C&&(C[O].dispose(),delete C[O])}}}function VE(n,e){function t(){let W=!1,Te=new $t,oe=null,Re=new $t(0,0,0,0);return{setMask:function(He){oe!==He&&!W&&(n.colorMask(He,He,He,He),oe=He)},setLocked:function(He){W=He},setClear:function(He,ve,st,Je,Xt){Xt===!0&&(He*=Je,ve*=Je,st*=Je),Te.set(He,ve,st,Je),Re.equals(Te)===!1&&(n.clearColor(He,ve,st,Je),Re.copy(Te))},reset:function(){W=!1,oe=null,Re.set(-1,0,0,0)}}}function i(){let W=!1,Te=!1,oe=null,Re=null,He=null;return{setReversed:function(ve){if(Te!==ve){let st=e.get("EXT_clip_control");ve?st.clipControlEXT(st.LOWER_LEFT_EXT,st.ZERO_TO_ONE_EXT):st.clipControlEXT(st.LOWER_LEFT_EXT,st.NEGATIVE_ONE_TO_ONE_EXT),Te=ve;let Je=He;He=null,this.setClear(Je)}},getReversed:function(){return Te},setTest:function(ve){ve?me(n.DEPTH_TEST):qe(n.DEPTH_TEST)},setMask:function(ve){oe!==ve&&!W&&(n.depthMask(ve),oe=ve)},setFunc:function(ve){if(Te&&(ve=s0[ve]),Re!==ve){switch(ve){case Bc:n.depthFunc(n.NEVER);break;case Hc:n.depthFunc(n.ALWAYS);break;case kc:n.depthFunc(n.LESS);break;case Go:n.depthFunc(n.LEQUAL);break;case Vc:n.depthFunc(n.EQUAL);break;case zc:n.depthFunc(n.GEQUAL);break;case Gc:n.depthFunc(n.GREATER);break;case Wc:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}Re=ve}},setLocked:function(ve){W=ve},setClear:function(ve){He!==ve&&(He=ve,Te&&(ve=1-ve),n.clearDepth(ve))},reset:function(){W=!1,oe=null,Re=null,He=null,Te=!1}}}function s(){let W=!1,Te=null,oe=null,Re=null,He=null,ve=null,st=null,Je=null,Xt=null;return{setTest:function(De){W||(De?me(n.STENCIL_TEST):qe(n.STENCIL_TEST))},setMask:function(De){Te!==De&&!W&&(n.stencilMask(De),Te=De)},setFunc:function(De,On,Jn){(oe!==De||Re!==On||He!==Jn)&&(n.stencilFunc(De,On,Jn),oe=De,Re=On,He=Jn)},setOp:function(De,On,Jn){(ve!==De||st!==On||Je!==Jn)&&(n.stencilOp(De,On,Jn),ve=De,st=On,Je=Jn)},setLocked:function(De){W=De},setClear:function(De){Xt!==De&&(n.clearStencil(De),Xt=De)},reset:function(){W=!1,Te=null,oe=null,Re=null,He=null,ve=null,st=null,Je=null,Xt=null}}}let r=new t,o=new i,a=new s,c=new WeakMap,l=new WeakMap,u={},d={},f={},p=new WeakMap,x=[],b=null,g=!1,m=null,A=null,U=null,T=null,I=null,L=null,P=null,M=new ke(0,0,0),C=0,O=!1,H=null,k=null,q=null,z=null,ee=null,he=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS),ue=!1,ye=0,V=n.getParameter(n.VERSION);V.indexOf("WebGL")!==-1?(ye=parseFloat(/^WebGL (\d)/.exec(V)[1]),ue=ye>=1):V.indexOf("OpenGL ES")!==-1&&(ye=parseFloat(/^OpenGL ES (\d)/.exec(V)[1]),ue=ye>=2);let Q=null,le={},Ee=n.getParameter(n.SCISSOR_BOX),be=n.getParameter(n.VIEWPORT),ut=new $t().fromArray(Ee),et=new $t().fromArray(be);function ct(W,Te,oe,Re){let He=new Uint8Array(4),ve=n.createTexture();n.bindTexture(W,ve),n.texParameteri(W,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(W,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let st=0;st<oe;st++)W===n.TEXTURE_3D||W===n.TEXTURE_2D_ARRAY?n.texImage3D(Te,0,n.RGBA,1,1,Re,0,n.RGBA,n.UNSIGNED_BYTE,He):n.texImage2D(Te+st,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,He);return ve}let ae={};ae[n.TEXTURE_2D]=ct(n.TEXTURE_2D,n.TEXTURE_2D,1),ae[n.TEXTURE_CUBE_MAP]=ct(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ae[n.TEXTURE_2D_ARRAY]=ct(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ae[n.TEXTURE_3D]=ct(n.TEXTURE_3D,n.TEXTURE_3D,1,1),r.setClear(0,0,0,1),o.setClear(1),a.setClear(0),me(n.DEPTH_TEST),o.setFunc(Go),Tt(!1),Jt(Sd),me(n.CULL_FACE),Ft(bs);function me(W){u[W]!==!0&&(n.enable(W),u[W]=!0)}function qe(W){u[W]!==!1&&(n.disable(W),u[W]=!1)}function ft(W,Te){return f[W]!==Te?(n.bindFramebuffer(W,Te),f[W]=Te,W===n.DRAW_FRAMEBUFFER&&(f[n.FRAMEBUFFER]=Te),W===n.FRAMEBUFFER&&(f[n.DRAW_FRAMEBUFFER]=Te),!0):!1}function Ge(W,Te){let oe=x,Re=!1;if(W){oe=p.get(Te),oe===void 0&&(oe=[],p.set(Te,oe));let He=W.textures;if(oe.length!==He.length||oe[0]!==n.COLOR_ATTACHMENT0){for(let ve=0,st=He.length;ve<st;ve++)oe[ve]=n.COLOR_ATTACHMENT0+ve;oe.length=He.length,Re=!0}}else oe[0]!==n.BACK&&(oe[0]=n.BACK,Re=!0);Re&&n.drawBuffers(oe)}function Et(W){return b!==W?(n.useProgram(W),b=W,!0):!1}let pn={[eo]:n.FUNC_ADD,[Sm]:n.FUNC_SUBTRACT,[wm]:n.FUNC_REVERSE_SUBTRACT};pn[Am]=n.MIN,pn[Rm]=n.MAX;let bt={[Cm]:n.ZERO,[Im]:n.ONE,[Pm]:n.SRC_COLOR,[Rd]:n.SRC_ALPHA,[Om]:n.SRC_ALPHA_SATURATE,[Um]:n.DST_COLOR,[Dm]:n.DST_ALPHA,[Lm]:n.ONE_MINUS_SRC_COLOR,[Cd]:n.ONE_MINUS_SRC_ALPHA,[Fm]:n.ONE_MINUS_DST_COLOR,[Nm]:n.ONE_MINUS_DST_ALPHA,[Bm]:n.CONSTANT_COLOR,[Hm]:n.ONE_MINUS_CONSTANT_COLOR,[km]:n.CONSTANT_ALPHA,[Vm]:n.ONE_MINUS_CONSTANT_ALPHA};function Ft(W,Te,oe,Re,He,ve,st,Je,Xt,De){if(W===bs){g===!0&&(qe(n.BLEND),g=!1);return}if(g===!1&&(me(n.BLEND),g=!0),W!==Tm){if(W!==m||De!==O){if((A!==eo||I!==eo)&&(n.blendEquation(n.FUNC_ADD),A=eo,I=eo),De)switch(W){case Ui:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case oa:n.blendFunc(n.ONE,n.ONE);break;case wd:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case Ad:n.blendFuncSeparate(n.DST_COLOR,n.ONE_MINUS_SRC_ALPHA,n.ZERO,n.ONE);break;default:ht("WebGLState: Invalid blending: ",W);break}else switch(W){case Ui:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case oa:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE,n.ONE,n.ONE);break;case wd:ht("WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case Ad:ht("WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:ht("WebGLState: Invalid blending: ",W);break}U=null,T=null,L=null,P=null,M.set(0,0,0),C=0,m=W,O=De}return}He=He||Te,ve=ve||oe,st=st||Re,(Te!==A||He!==I)&&(n.blendEquationSeparate(pn[Te],pn[He]),A=Te,I=He),(oe!==U||Re!==T||ve!==L||st!==P)&&(n.blendFuncSeparate(bt[oe],bt[Re],bt[ve],bt[st]),U=oe,T=Re,L=ve,P=st),(Je.equals(M)===!1||Xt!==C)&&(n.blendColor(Je.r,Je.g,Je.b,Xt),M.copy(Je),C=Xt),m=W,O=!1}function Wt(W,Te){W.side===mn?qe(n.CULL_FACE):me(n.CULL_FACE);let oe=W.side===Hn;Te&&(oe=!oe),Tt(oe),W.blending===Ui&&W.transparent===!1?Ft(bs):Ft(W.blending,W.blendEquation,W.blendSrc,W.blendDst,W.blendEquationAlpha,W.blendSrcAlpha,W.blendDstAlpha,W.blendColor,W.blendAlpha,W.premultipliedAlpha),o.setFunc(W.depthFunc),o.setTest(W.depthTest),o.setMask(W.depthWrite),r.setMask(W.colorWrite);let Re=W.stencilWrite;a.setTest(Re),Re&&(a.setMask(W.stencilWriteMask),a.setFunc(W.stencilFunc,W.stencilRef,W.stencilFuncMask),a.setOp(W.stencilFail,W.stencilZFail,W.stencilZPass)),xe(W.polygonOffset,W.polygonOffsetFactor,W.polygonOffsetUnits),W.alphaToCoverage===!0?me(n.SAMPLE_ALPHA_TO_COVERAGE):qe(n.SAMPLE_ALPHA_TO_COVERAGE)}function Tt(W){H!==W&&(W?n.frontFace(n.CW):n.frontFace(n.CCW),H=W)}function Jt(W){W!==Em?(me(n.CULL_FACE),W!==k&&(W===Sd?n.cullFace(n.BACK):W===bm?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):qe(n.CULL_FACE),k=W}function bn(W){W!==q&&(ue&&n.lineWidth(W),q=W)}function xe(W,Te,oe){W?(me(n.POLYGON_OFFSET_FILL),(z!==Te||ee!==oe)&&(z=Te,ee=oe,o.getReversed()&&(Te=-Te),n.polygonOffset(Te,oe))):qe(n.POLYGON_OFFSET_FILL)}function vt(W){W?me(n.SCISSOR_TEST):qe(n.SCISSOR_TEST)}function Rt(W){W===void 0&&(W=n.TEXTURE0+he-1),Q!==W&&(n.activeTexture(W),Q=W)}function X(W,Te,oe){oe===void 0&&(Q===null?oe=n.TEXTURE0+he-1:oe=Q);let Re=le[oe];Re===void 0&&(Re={type:void 0,texture:void 0},le[oe]=Re),(Re.type!==W||Re.texture!==Te)&&(Q!==oe&&(n.activeTexture(oe),Q=oe),n.bindTexture(W,Te||ae[W]),Re.type=W,Re.texture=Te)}function xn(){let W=le[Q];W!==void 0&&W.type!==void 0&&(n.bindTexture(W.type,null),W.type=void 0,W.texture=void 0)}function lt(){try{n.compressedTexImage2D(...arguments)}catch(W){ht("WebGLState:",W)}}function B(){try{n.compressedTexImage3D(...arguments)}catch(W){ht("WebGLState:",W)}}function E(){try{n.texSubImage2D(...arguments)}catch(W){ht("WebGLState:",W)}}function $(){try{n.texSubImage3D(...arguments)}catch(W){ht("WebGLState:",W)}}function se(){try{n.compressedTexSubImage2D(...arguments)}catch(W){ht("WebGLState:",W)}}function de(){try{n.compressedTexSubImage3D(...arguments)}catch(W){ht("WebGLState:",W)}}function we(){try{n.texStorage2D(...arguments)}catch(W){ht("WebGLState:",W)}}function Ae(){try{n.texStorage3D(...arguments)}catch(W){ht("WebGLState:",W)}}function ce(){try{n.texImage2D(...arguments)}catch(W){ht("WebGLState:",W)}}function re(){try{n.texImage3D(...arguments)}catch(W){ht("WebGLState:",W)}}function Ie(W){return d[W]!==void 0?d[W]:n.getParameter(W)}function Ze(W,Te){d[W]!==Te&&(n.pixelStorei(W,Te),d[W]=Te)}function Fe(W){ut.equals(W)===!1&&(n.scissor(W.x,W.y,W.z,W.w),ut.copy(W))}function Se(W){et.equals(W)===!1&&(n.viewport(W.x,W.y,W.z,W.w),et.copy(W))}function it(W,Te){let oe=l.get(Te);oe===void 0&&(oe=new WeakMap,l.set(Te,oe));let Re=oe.get(W);Re===void 0&&(Re=n.getUniformBlockIndex(Te,W.name),oe.set(W,Re))}function ot(W,Te){let Re=l.get(Te).get(W);c.get(Te)!==Re&&(n.uniformBlockBinding(Te,Re,W.__bindingPointIndex),c.set(Te,Re))}function xt(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),o.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),n.pixelStorei(n.PACK_ALIGNMENT,4),n.pixelStorei(n.UNPACK_ALIGNMENT,4),n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,!1),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,!1),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,n.BROWSER_DEFAULT_WEBGL),n.pixelStorei(n.PACK_ROW_LENGTH,0),n.pixelStorei(n.PACK_SKIP_PIXELS,0),n.pixelStorei(n.PACK_SKIP_ROWS,0),n.pixelStorei(n.UNPACK_ROW_LENGTH,0),n.pixelStorei(n.UNPACK_IMAGE_HEIGHT,0),n.pixelStorei(n.UNPACK_SKIP_PIXELS,0),n.pixelStorei(n.UNPACK_SKIP_ROWS,0),n.pixelStorei(n.UNPACK_SKIP_IMAGES,0),u={},d={},Q=null,le={},f={},p=new WeakMap,x=[],b=null,g=!1,m=null,A=null,U=null,T=null,I=null,L=null,P=null,M=new ke(0,0,0),C=0,O=!1,H=null,k=null,q=null,z=null,ee=null,ut.set(0,0,n.canvas.width,n.canvas.height),et.set(0,0,n.canvas.width,n.canvas.height),r.reset(),o.reset(),a.reset()}return{buffers:{color:r,depth:o,stencil:a},enable:me,disable:qe,bindFramebuffer:ft,drawBuffers:Ge,useProgram:Et,setBlending:Ft,setMaterial:Wt,setFlipSided:Tt,setCullFace:Jt,setLineWidth:bn,setPolygonOffset:xe,setScissorTest:vt,activeTexture:Rt,bindTexture:X,unbindTexture:xn,compressedTexImage2D:lt,compressedTexImage3D:B,texImage2D:ce,texImage3D:re,pixelStorei:Ze,getParameter:Ie,updateUBOMapping:it,uniformBlockBinding:ot,texStorage2D:we,texStorage3D:Ae,texSubImage2D:E,texSubImage3D:$,compressedTexSubImage2D:se,compressedTexSubImage3D:de,scissor:Fe,viewport:Se,reset:xt}}function zE(n,e,t,i,s,r,o){let a=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new Pe,u=new WeakMap,d=new Set,f,p=new WeakMap,x=!1;try{x=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function b(B,E){return x?new OffscreenCanvas(B,E):qo("canvas")}function g(B,E,$){let se=1,de=lt(B);if((de.width>$||de.height>$)&&(se=$/Math.max(de.width,de.height)),se<1)if(typeof HTMLImageElement<"u"&&B instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&B instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&B instanceof ImageBitmap||typeof VideoFrame<"u"&&B instanceof VideoFrame){let we=Math.floor(se*de.width),Ae=Math.floor(se*de.height);f===void 0&&(f=b(we,Ae));let ce=E?b(we,Ae):f;return ce.width=we,ce.height=Ae,ce.getContext("2d").drawImage(B,0,0,we,Ae),nt("WebGLRenderer: Texture has been resized from ("+de.width+"x"+de.height+") to ("+we+"x"+Ae+")."),ce}else return"data"in B&&nt("WebGLRenderer: Image in DataTexture is too big ("+de.width+"x"+de.height+")."),B;return B}function m(B){return B.generateMipmaps}function A(B){n.generateMipmap(B)}function U(B){return B.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:B.isWebGL3DRenderTarget?n.TEXTURE_3D:B.isWebGLArrayRenderTarget||B.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function T(B,E,$,se,de,we=!1){if(B!==null){if(n[B]!==void 0)return n[B];nt("WebGLRenderer: Attempt to use non-existing WebGL internal format '"+B+"'")}let Ae;se&&(Ae=e.get("EXT_texture_norm16"),Ae||nt("WebGLRenderer: Unable to use normalized textures without EXT_texture_norm16 extension"));let ce=E;if(E===n.RED&&($===n.FLOAT&&(ce=n.R32F),$===n.HALF_FLOAT&&(ce=n.R16F),$===n.UNSIGNED_BYTE&&(ce=n.R8),$===n.UNSIGNED_SHORT&&Ae&&(ce=Ae.R16_EXT),$===n.SHORT&&Ae&&(ce=Ae.R16_SNORM_EXT)),E===n.RED_INTEGER&&($===n.UNSIGNED_BYTE&&(ce=n.R8UI),$===n.UNSIGNED_SHORT&&(ce=n.R16UI),$===n.UNSIGNED_INT&&(ce=n.R32UI),$===n.BYTE&&(ce=n.R8I),$===n.SHORT&&(ce=n.R16I),$===n.INT&&(ce=n.R32I)),E===n.RG&&($===n.FLOAT&&(ce=n.RG32F),$===n.HALF_FLOAT&&(ce=n.RG16F),$===n.UNSIGNED_BYTE&&(ce=n.RG8),$===n.UNSIGNED_SHORT&&Ae&&(ce=Ae.RG16_EXT),$===n.SHORT&&Ae&&(ce=Ae.RG16_SNORM_EXT)),E===n.RG_INTEGER&&($===n.UNSIGNED_BYTE&&(ce=n.RG8UI),$===n.UNSIGNED_SHORT&&(ce=n.RG16UI),$===n.UNSIGNED_INT&&(ce=n.RG32UI),$===n.BYTE&&(ce=n.RG8I),$===n.SHORT&&(ce=n.RG16I),$===n.INT&&(ce=n.RG32I)),E===n.RGB_INTEGER&&($===n.UNSIGNED_BYTE&&(ce=n.RGB8UI),$===n.UNSIGNED_SHORT&&(ce=n.RGB16UI),$===n.UNSIGNED_INT&&(ce=n.RGB32UI),$===n.BYTE&&(ce=n.RGB8I),$===n.SHORT&&(ce=n.RGB16I),$===n.INT&&(ce=n.RGB32I)),E===n.RGBA_INTEGER&&($===n.UNSIGNED_BYTE&&(ce=n.RGBA8UI),$===n.UNSIGNED_SHORT&&(ce=n.RGBA16UI),$===n.UNSIGNED_INT&&(ce=n.RGBA32UI),$===n.BYTE&&(ce=n.RGBA8I),$===n.SHORT&&(ce=n.RGBA16I),$===n.INT&&(ce=n.RGBA32I)),E===n.RGB&&($===n.UNSIGNED_SHORT&&Ae&&(ce=Ae.RGB16_EXT),$===n.SHORT&&Ae&&(ce=Ae.RGB16_SNORM_EXT),$===n.UNSIGNED_INT_5_9_9_9_REV&&(ce=n.RGB9_E5),$===n.UNSIGNED_INT_10F_11F_11F_REV&&(ce=n.R11F_G11F_B10F)),E===n.RGBA){let re=we?Ka:It.getTransfer(de);$===n.FLOAT&&(ce=n.RGBA32F),$===n.HALF_FLOAT&&(ce=n.RGBA16F),$===n.UNSIGNED_BYTE&&(ce=re===Gt?n.SRGB8_ALPHA8:n.RGBA8),$===n.UNSIGNED_SHORT&&Ae&&(ce=Ae.RGBA16_EXT),$===n.SHORT&&Ae&&(ce=Ae.RGBA16_SNORM_EXT),$===n.UNSIGNED_SHORT_4_4_4_4&&(ce=n.RGBA4),$===n.UNSIGNED_SHORT_5_5_5_1&&(ce=n.RGB5_A1)}return(ce===n.R16F||ce===n.R32F||ce===n.RG16F||ce===n.RG32F||ce===n.RGBA16F||ce===n.RGBA32F)&&e.get("EXT_color_buffer_float"),ce}function I(B,E){let $;return B?E===null||E===ss||E===ca?$=n.DEPTH24_STENCIL8:E===Ti?$=n.DEPTH32F_STENCIL8:E===la&&($=n.DEPTH24_STENCIL8,nt("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):E===null||E===ss||E===ca?$=n.DEPTH_COMPONENT24:E===Ti?$=n.DEPTH_COMPONENT32F:E===la&&($=n.DEPTH_COMPONENT16),$}function L(B,E){return m(B)===!0||B.isFramebufferTexture&&B.minFilter!==vn&&B.minFilter!==yn?Math.log2(Math.max(E.width,E.height))+1:B.mipmaps!==void 0&&B.mipmaps.length>0?B.mipmaps.length:B.isCompressedTexture&&Array.isArray(B.image)?E.mipmaps.length:1}function P(B){let E=B.target;E.removeEventListener("dispose",P),C(E),E.isVideoTexture&&u.delete(E),E.isHTMLTexture&&d.delete(E)}function M(B){let E=B.target;E.removeEventListener("dispose",M),H(E)}function C(B){let E=i.get(B);if(E.__webglInit===void 0)return;let $=B.source,se=p.get($);if(se){let de=se[E.__cacheKey];de.usedTimes--,de.usedTimes===0&&O(B),Object.keys(se).length===0&&p.delete($)}i.remove(B)}function O(B){let E=i.get(B);n.deleteTexture(E.__webglTexture);let $=B.source,se=p.get($);delete se[E.__cacheKey],o.memory.textures--}function H(B){let E=i.get(B);if(B.depthTexture&&(B.depthTexture.dispose(),i.remove(B.depthTexture)),B.isWebGLCubeRenderTarget)for(let se=0;se<6;se++){if(Array.isArray(E.__webglFramebuffer[se]))for(let de=0;de<E.__webglFramebuffer[se].length;de++)n.deleteFramebuffer(E.__webglFramebuffer[se][de]);else n.deleteFramebuffer(E.__webglFramebuffer[se]);E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer[se])}else{if(Array.isArray(E.__webglFramebuffer))for(let se=0;se<E.__webglFramebuffer.length;se++)n.deleteFramebuffer(E.__webglFramebuffer[se]);else n.deleteFramebuffer(E.__webglFramebuffer);if(E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer),E.__webglMultisampledFramebuffer&&n.deleteFramebuffer(E.__webglMultisampledFramebuffer),E.__webglColorRenderbuffer)for(let se=0;se<E.__webglColorRenderbuffer.length;se++)E.__webglColorRenderbuffer[se]&&n.deleteRenderbuffer(E.__webglColorRenderbuffer[se]);E.__webglDepthRenderbuffer&&n.deleteRenderbuffer(E.__webglDepthRenderbuffer)}let $=B.textures;for(let se=0,de=$.length;se<de;se++){let we=i.get($[se]);we.__webglTexture&&(n.deleteTexture(we.__webglTexture),o.memory.textures--),i.remove($[se])}i.remove(B)}let k=0;function q(){k=0}function z(){return k}function ee(B){k=B}function he(){let B=k;return B>=s.maxTextures&&nt("WebGLTextures: Trying to use "+(B+1)+" texture units while this GPU supports only "+s.maxTextures),k+=1,B}function ue(B){let E=[];return E.push(B.wrapS),E.push(B.wrapT),E.push(B.wrapR||0),E.push(B.magFilter),E.push(B.minFilter),E.push(B.anisotropy),E.push(B.internalFormat),E.push(B.format),E.push(B.type),E.push(B.generateMipmaps),E.push(B.premultiplyAlpha),E.push(B.flipY),E.push(B.unpackAlignment),E.push(B.colorSpace),E.join()}function ye(B,E){let $=i.get(B);if(B.isVideoTexture&&X(B),B.isRenderTargetTexture===!1&&B.isExternalTexture!==!0&&B.version>0&&$.__version!==B.version){let se=B.image;if(se===null)nt("WebGLRenderer: Texture marked for update but no image data found.");else if(se.complete===!1)nt("WebGLRenderer: Texture marked for update but image is incomplete");else{qe($,B,E);return}}else B.isExternalTexture&&($.__webglTexture=B.sourceTexture?B.sourceTexture:null);t.bindTexture(n.TEXTURE_2D,$.__webglTexture,n.TEXTURE0+E)}function V(B,E){let $=i.get(B);if(B.isRenderTargetTexture===!1&&B.version>0&&$.__version!==B.version){qe($,B,E);return}else B.isExternalTexture&&($.__webglTexture=B.sourceTexture?B.sourceTexture:null);t.bindTexture(n.TEXTURE_2D_ARRAY,$.__webglTexture,n.TEXTURE0+E)}function Q(B,E){let $=i.get(B);if(B.isRenderTargetTexture===!1&&B.version>0&&$.__version!==B.version){qe($,B,E);return}t.bindTexture(n.TEXTURE_3D,$.__webglTexture,n.TEXTURE0+E)}function le(B,E){let $=i.get(B);if(B.isCubeDepthTexture!==!0&&B.version>0&&$.__version!==B.version){ft($,B,E);return}t.bindTexture(n.TEXTURE_CUBE_MAP,$.__webglTexture,n.TEXTURE0+E)}let Ee={[oi]:n.REPEAT,[Ii]:n.CLAMP_TO_EDGE,[Wo]:n.MIRRORED_REPEAT},be={[vn]:n.NEAREST,[vh]:n.NEAREST_MIPMAP_NEAREST,[no]:n.NEAREST_MIPMAP_LINEAR,[yn]:n.LINEAR,[aa]:n.LINEAR_MIPMAP_NEAREST,[is]:n.LINEAR_MIPMAP_LINEAR},ut={[Zm]:n.NEVER,[e0]:n.ALWAYS,[Km]:n.LESS,[su]:n.LEQUAL,[jm]:n.EQUAL,[ru]:n.GEQUAL,[Jm]:n.GREATER,[Qm]:n.NOTEQUAL};function et(B,E){if(E.type===Ti&&e.has("OES_texture_float_linear")===!1&&(E.magFilter===yn||E.magFilter===aa||E.magFilter===no||E.magFilter===is||E.minFilter===yn||E.minFilter===aa||E.minFilter===no||E.minFilter===is)&&nt("WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(B,n.TEXTURE_WRAP_S,Ee[E.wrapS]),n.texParameteri(B,n.TEXTURE_WRAP_T,Ee[E.wrapT]),(B===n.TEXTURE_3D||B===n.TEXTURE_2D_ARRAY)&&n.texParameteri(B,n.TEXTURE_WRAP_R,Ee[E.wrapR]),n.texParameteri(B,n.TEXTURE_MAG_FILTER,be[E.magFilter]),n.texParameteri(B,n.TEXTURE_MIN_FILTER,be[E.minFilter]),E.compareFunction&&(n.texParameteri(B,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(B,n.TEXTURE_COMPARE_FUNC,ut[E.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(E.magFilter===vn||E.minFilter!==no&&E.minFilter!==is||E.type===Ti&&e.has("OES_texture_float_linear")===!1)return;if(E.anisotropy>1||i.get(E).__currentAnisotropy){let $=e.get("EXT_texture_filter_anisotropic");n.texParameterf(B,$.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(E.anisotropy,s.getMaxAnisotropy())),i.get(E).__currentAnisotropy=E.anisotropy}}}function ct(B,E){let $=!1;B.__webglInit===void 0&&(B.__webglInit=!0,E.addEventListener("dispose",P));let se=E.source,de=p.get(se);de===void 0&&(de={},p.set(se,de));let we=ue(E);if(we!==B.__cacheKey){de[we]===void 0&&(de[we]={texture:n.createTexture(),usedTimes:0},o.memory.textures++,$=!0),de[we].usedTimes++;let Ae=de[B.__cacheKey];Ae!==void 0&&(de[B.__cacheKey].usedTimes--,Ae.usedTimes===0&&O(E)),B.__cacheKey=we,B.__webglTexture=de[we].texture}return $}function ae(B,E,$){return Math.floor(Math.floor(B/$)/E)}function me(B,E,$,se){let we=B.updateRanges;if(we.length===0)t.texSubImage2D(n.TEXTURE_2D,0,0,0,E.width,E.height,$,se,E.data);else{we.sort((Ze,Fe)=>Ze.start-Fe.start);let Ae=0;for(let Ze=1;Ze<we.length;Ze++){let Fe=we[Ae],Se=we[Ze],it=Fe.start+Fe.count,ot=ae(Se.start,E.width,4),xt=ae(Fe.start,E.width,4);Se.start<=it+1&&ot===xt&&ae(Se.start+Se.count-1,E.width,4)===ot?Fe.count=Math.max(Fe.count,Se.start+Se.count-Fe.start):(++Ae,we[Ae]=Se)}we.length=Ae+1;let ce=t.getParameter(n.UNPACK_ROW_LENGTH),re=t.getParameter(n.UNPACK_SKIP_PIXELS),Ie=t.getParameter(n.UNPACK_SKIP_ROWS);t.pixelStorei(n.UNPACK_ROW_LENGTH,E.width);for(let Ze=0,Fe=we.length;Ze<Fe;Ze++){let Se=we[Ze],it=Math.floor(Se.start/4),ot=Math.ceil(Se.count/4),xt=it%E.width,W=Math.floor(it/E.width),Te=ot,oe=1;t.pixelStorei(n.UNPACK_SKIP_PIXELS,xt),t.pixelStorei(n.UNPACK_SKIP_ROWS,W),t.texSubImage2D(n.TEXTURE_2D,0,xt,W,Te,oe,$,se,E.data)}B.clearUpdateRanges(),t.pixelStorei(n.UNPACK_ROW_LENGTH,ce),t.pixelStorei(n.UNPACK_SKIP_PIXELS,re),t.pixelStorei(n.UNPACK_SKIP_ROWS,Ie)}}function qe(B,E,$){let se=n.TEXTURE_2D;(E.isDataArrayTexture||E.isCompressedArrayTexture)&&(se=n.TEXTURE_2D_ARRAY),E.isData3DTexture&&(se=n.TEXTURE_3D);let de=ct(B,E),we=E.source;t.bindTexture(se,B.__webglTexture,n.TEXTURE0+$);let Ae=i.get(we);if(we.version!==Ae.__version||de===!0){if(t.activeTexture(n.TEXTURE0+$),(typeof ImageBitmap<"u"&&E.image instanceof ImageBitmap)===!1){let oe=It.getPrimaries(It.workingColorSpace),Re=E.colorSpace===$s?null:It.getPrimaries(E.colorSpace),He=E.colorSpace===$s||oe===Re?n.NONE:n.BROWSER_DEFAULT_WEBGL;t.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),t.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),t.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,He)}t.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment);let re=g(E.image,!1,s.maxTextureSize);re=xn(E,re);let Ie=r.convert(E.format,E.colorSpace),Ze=r.convert(E.type),Fe=T(E.internalFormat,Ie,Ze,E.normalized,E.colorSpace,E.isVideoTexture);et(se,E);let Se,it=E.mipmaps,ot=E.isVideoTexture!==!0,xt=Ae.__version===void 0||de===!0,W=we.dataReady,Te=L(E,re);if(E.isDepthTexture)Fe=I(E.format===_r,E.type),xt&&(ot?t.texStorage2D(n.TEXTURE_2D,1,Fe,re.width,re.height):t.texImage2D(n.TEXTURE_2D,0,Fe,re.width,re.height,0,Ie,Ze,null));else if(E.isDataTexture)if(it.length>0){ot&&xt&&t.texStorage2D(n.TEXTURE_2D,Te,Fe,it[0].width,it[0].height);for(let oe=0,Re=it.length;oe<Re;oe++)Se=it[oe],ot?W&&t.texSubImage2D(n.TEXTURE_2D,oe,0,0,Se.width,Se.height,Ie,Ze,Se.data):t.texImage2D(n.TEXTURE_2D,oe,Fe,Se.width,Se.height,0,Ie,Ze,Se.data);E.generateMipmaps=!1}else ot?(xt&&t.texStorage2D(n.TEXTURE_2D,Te,Fe,re.width,re.height),W&&me(E,re,Ie,Ze)):t.texImage2D(n.TEXTURE_2D,0,Fe,re.width,re.height,0,Ie,Ze,re.data);else if(E.isCompressedTexture)if(E.isCompressedArrayTexture){ot&&xt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,Te,Fe,it[0].width,it[0].height,re.depth);for(let oe=0,Re=it.length;oe<Re;oe++)if(Se=it[oe],E.format!==Si)if(Ie!==null)if(ot){if(W)if(E.layerUpdates.size>0){let He=Jd(Se.width,Se.height,E.format,E.type);for(let ve of E.layerUpdates){let st=Se.data.subarray(ve*He/Se.data.BYTES_PER_ELEMENT,(ve+1)*He/Se.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,oe,0,0,ve,Se.width,Se.height,1,Ie,st)}}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,oe,0,0,0,Se.width,Se.height,re.depth,Ie,Se.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,oe,Fe,Se.width,Se.height,re.depth,0,Se.data,0,0);else nt("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else ot?W&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,oe,0,0,0,Se.width,Se.height,re.depth,Ie,Ze,Se.data):t.texImage3D(n.TEXTURE_2D_ARRAY,oe,Fe,Se.width,Se.height,re.depth,0,Ie,Ze,Se.data);E.layerUpdates.size>0&&E.clearLayerUpdates()}else{ot&&xt&&t.texStorage2D(n.TEXTURE_2D,Te,Fe,it[0].width,it[0].height);for(let oe=0,Re=it.length;oe<Re;oe++)Se=it[oe],E.format!==Si?Ie!==null?ot?W&&t.compressedTexSubImage2D(n.TEXTURE_2D,oe,0,0,Se.width,Se.height,Ie,Se.data):t.compressedTexImage2D(n.TEXTURE_2D,oe,Fe,Se.width,Se.height,0,Se.data):nt("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):ot?W&&t.texSubImage2D(n.TEXTURE_2D,oe,0,0,Se.width,Se.height,Ie,Ze,Se.data):t.texImage2D(n.TEXTURE_2D,oe,Fe,Se.width,Se.height,0,Ie,Ze,Se.data)}else if(E.isDataArrayTexture)if(ot){if(xt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,Te,Fe,re.width,re.height,re.depth),W)if(E.layerUpdates.size>0){let oe=Jd(re.width,re.height,E.format,E.type);for(let Re of E.layerUpdates){let He=re.data.subarray(Re*oe/re.data.BYTES_PER_ELEMENT,(Re+1)*oe/re.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,Re,re.width,re.height,1,Ie,Ze,He)}E.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,re.width,re.height,re.depth,Ie,Ze,re.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,Fe,re.width,re.height,re.depth,0,Ie,Ze,re.data);else if(E.isData3DTexture)ot?(xt&&t.texStorage3D(n.TEXTURE_3D,Te,Fe,re.width,re.height,re.depth),W&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,re.width,re.height,re.depth,Ie,Ze,re.data)):t.texImage3D(n.TEXTURE_3D,0,Fe,re.width,re.height,re.depth,0,Ie,Ze,re.data);else if(E.isFramebufferTexture){if(xt)if(ot)t.texStorage2D(n.TEXTURE_2D,Te,Fe,re.width,re.height);else{let oe=re.width,Re=re.height;for(let He=0;He<Te;He++)t.texImage2D(n.TEXTURE_2D,He,Fe,oe,Re,0,Ie,Ze,null),oe>>=1,Re>>=1}}else if(E.isHTMLTexture){if("texElementImage2D"in n){let oe=n.canvas;if(oe.hasAttribute("layoutsubtree")||oe.setAttribute("layoutsubtree","true"),re.parentNode!==oe){oe.appendChild(re),d.add(E),oe.onpaint=Re=>{let He=Re.changedElements;for(let ve of d)He.includes(ve.image)&&(ve.needsUpdate=!0)},oe.requestPaint();return}if(n.texElementImage2D.length===3)n.texElementImage2D(n.TEXTURE_2D,n.RGBA8,re);else{let He=n.RGBA,ve=n.RGBA,st=n.UNSIGNED_BYTE;n.texElementImage2D(n.TEXTURE_2D,0,He,ve,st,re)}n.texParameteri(n.TEXTURE_2D,n.TEXTURE_MIN_FILTER,n.LINEAR),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_S,n.CLAMP_TO_EDGE),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_T,n.CLAMP_TO_EDGE)}}else if(it.length>0){if(ot&&xt){let oe=lt(it[0]);t.texStorage2D(n.TEXTURE_2D,Te,Fe,oe.width,oe.height)}for(let oe=0,Re=it.length;oe<Re;oe++)Se=it[oe],ot?W&&t.texSubImage2D(n.TEXTURE_2D,oe,0,0,Ie,Ze,Se):t.texImage2D(n.TEXTURE_2D,oe,Fe,Ie,Ze,Se);E.generateMipmaps=!1}else if(ot){if(xt){let oe=lt(re);t.texStorage2D(n.TEXTURE_2D,Te,Fe,oe.width,oe.height)}W&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,Ie,Ze,re)}else t.texImage2D(n.TEXTURE_2D,0,Fe,Ie,Ze,re);m(E)&&A(se),Ae.__version=we.version,E.onUpdate&&E.onUpdate(E)}B.__version=E.version}function ft(B,E,$){if(E.image.length!==6)return;let se=ct(B,E),de=E.source;t.bindTexture(n.TEXTURE_CUBE_MAP,B.__webglTexture,n.TEXTURE0+$);let we=i.get(de);if(de.version!==we.__version||se===!0){t.activeTexture(n.TEXTURE0+$);let Ae=It.getPrimaries(It.workingColorSpace),ce=E.colorSpace===$s?null:It.getPrimaries(E.colorSpace),re=E.colorSpace===$s||Ae===ce?n.NONE:n.BROWSER_DEFAULT_WEBGL;t.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),t.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),t.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment),t.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,re);let Ie=E.isCompressedTexture||E.image[0].isCompressedTexture,Ze=E.image[0]&&E.image[0].isDataTexture,Fe=[];for(let ve=0;ve<6;ve++)!Ie&&!Ze?Fe[ve]=g(E.image[ve],!0,s.maxCubemapSize):Fe[ve]=Ze?E.image[ve].image:E.image[ve],Fe[ve]=xn(E,Fe[ve]);let Se=Fe[0],it=r.convert(E.format,E.colorSpace),ot=r.convert(E.type),xt=T(E.internalFormat,it,ot,E.normalized,E.colorSpace),W=E.isVideoTexture!==!0,Te=we.__version===void 0||se===!0,oe=de.dataReady,Re=L(E,Se);et(n.TEXTURE_CUBE_MAP,E);let He;if(Ie){W&&Te&&t.texStorage2D(n.TEXTURE_CUBE_MAP,Re,xt,Se.width,Se.height);for(let ve=0;ve<6;ve++){He=Fe[ve].mipmaps;for(let st=0;st<He.length;st++){let Je=He[st];E.format!==Si?it!==null?W?oe&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st,0,0,Je.width,Je.height,it,Je.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st,xt,Je.width,Je.height,0,Je.data):nt("WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):W?oe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st,0,0,Je.width,Je.height,it,ot,Je.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st,xt,Je.width,Je.height,0,it,ot,Je.data)}}}else{if(He=E.mipmaps,W&&Te){He.length>0&&Re++;let ve=lt(Fe[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,Re,xt,ve.width,ve.height)}for(let ve=0;ve<6;ve++)if(Ze){W?oe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,0,0,0,Fe[ve].width,Fe[ve].height,it,ot,Fe[ve].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,0,xt,Fe[ve].width,Fe[ve].height,0,it,ot,Fe[ve].data);for(let st=0;st<He.length;st++){let Xt=He[st].image[ve].image;W?oe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st+1,0,0,Xt.width,Xt.height,it,ot,Xt.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st+1,xt,Xt.width,Xt.height,0,it,ot,Xt.data)}}else{W?oe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,0,0,0,it,ot,Fe[ve]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,0,xt,it,ot,Fe[ve]);for(let st=0;st<He.length;st++){let Je=He[st];W?oe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st+1,0,0,it,ot,Je.image[ve]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ve,st+1,xt,it,ot,Je.image[ve])}}}m(E)&&A(n.TEXTURE_CUBE_MAP),we.__version=de.version,E.onUpdate&&E.onUpdate(E)}B.__version=E.version}function Ge(B,E,$,se,de,we){let Ae=r.convert($.format,$.colorSpace),ce=r.convert($.type),re=T($.internalFormat,Ae,ce,$.normalized,$.colorSpace),Ie=i.get(E),Ze=i.get($);if(Ze.__renderTarget=E,!Ie.__hasExternalTextures){let Fe=Math.max(1,E.width>>we),Se=Math.max(1,E.height>>we);de===n.TEXTURE_3D||de===n.TEXTURE_2D_ARRAY?t.texImage3D(de,we,re,Fe,Se,E.depth,0,Ae,ce,null):t.texImage2D(de,we,re,Fe,Se,0,Ae,ce,null)}t.bindFramebuffer(n.FRAMEBUFFER,B),Rt(E)?a.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,se,de,Ze.__webglTexture,0,vt(E)):(de===n.TEXTURE_2D||de>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&de<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,se,de,Ze.__webglTexture,we),t.bindFramebuffer(n.FRAMEBUFFER,null)}function Et(B,E,$){if(n.bindRenderbuffer(n.RENDERBUFFER,B),E.depthBuffer){let se=E.depthTexture,de=se&&se.isDepthTexture?se.type:null,we=I(E.stencilBuffer,de),Ae=E.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;Rt(E)?a.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,vt(E),we,E.width,E.height):$?n.renderbufferStorageMultisample(n.RENDERBUFFER,vt(E),we,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,we,E.width,E.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Ae,n.RENDERBUFFER,B)}else{let se=E.textures;for(let de=0;de<se.length;de++){let we=se[de],Ae=r.convert(we.format,we.colorSpace),ce=r.convert(we.type),re=T(we.internalFormat,Ae,ce,we.normalized,we.colorSpace);Rt(E)?a.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,vt(E),re,E.width,E.height):$?n.renderbufferStorageMultisample(n.RENDERBUFFER,vt(E),re,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,re,E.width,E.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function pn(B,E,$){let se=E.isWebGLCubeRenderTarget===!0;if(t.bindFramebuffer(n.FRAMEBUFFER,B),!(E.depthTexture&&E.depthTexture.isDepthTexture))throw new Error("THREE.WebGLTextures: renderTarget.depthTexture must be an instance of THREE.DepthTexture.");let de=i.get(E.depthTexture);if(de.__renderTarget=E,(!de.__webglTexture||E.depthTexture.image.width!==E.width||E.depthTexture.image.height!==E.height)&&(E.depthTexture.image.width=E.width,E.depthTexture.image.height=E.height,E.depthTexture.needsUpdate=!0),se){if(de.__webglInit===void 0&&(de.__webglInit=!0,E.depthTexture.addEventListener("dispose",P)),de.__webglTexture===void 0){de.__webglTexture=n.createTexture(),t.bindTexture(n.TEXTURE_CUBE_MAP,de.__webglTexture),et(n.TEXTURE_CUBE_MAP,E.depthTexture);let Ie=r.convert(E.depthTexture.format),Ze=r.convert(E.depthTexture.type),Fe;E.depthTexture.format===xs?Fe=n.DEPTH_COMPONENT24:E.depthTexture.format===_r&&(Fe=n.DEPTH24_STENCIL8);for(let Se=0;Se<6;Se++)n.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+Se,0,Fe,E.width,E.height,0,Ie,Ze,null)}}else ye(E.depthTexture,0);let we=de.__webglTexture,Ae=vt(E),ce=se?n.TEXTURE_CUBE_MAP_POSITIVE_X+$:n.TEXTURE_2D,re=E.depthTexture.format===_r?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;if(E.depthTexture.format===xs)Rt(E)?a.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,re,ce,we,0,Ae):n.framebufferTexture2D(n.FRAMEBUFFER,re,ce,we,0);else if(E.depthTexture.format===_r)Rt(E)?a.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,re,ce,we,0,Ae):n.framebufferTexture2D(n.FRAMEBUFFER,re,ce,we,0);else throw new Error("THREE.WebGLTextures: Unknown depthTexture format.")}function bt(B){let E=i.get(B),$=B.isWebGLCubeRenderTarget===!0;if(E.__boundDepthTexture!==B.depthTexture){let se=B.depthTexture;if(E.__depthDisposeCallback&&E.__depthDisposeCallback(),se){let de=()=>{delete E.__boundDepthTexture,delete E.__depthDisposeCallback,se.removeEventListener("dispose",de)};se.addEventListener("dispose",de),E.__depthDisposeCallback=de}E.__boundDepthTexture=se}if(B.depthTexture&&!E.__autoAllocateDepthBuffer)if($)for(let se=0;se<6;se++)pn(E.__webglFramebuffer[se],B,se);else{let se=B.texture.mipmaps;se&&se.length>0?pn(E.__webglFramebuffer[0],B,0):pn(E.__webglFramebuffer,B,0)}else if($){E.__webglDepthbuffer=[];for(let se=0;se<6;se++)if(t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer[se]),E.__webglDepthbuffer[se]===void 0)E.__webglDepthbuffer[se]=n.createRenderbuffer(),Et(E.__webglDepthbuffer[se],B,!1);else{let de=B.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,we=E.__webglDepthbuffer[se];n.bindRenderbuffer(n.RENDERBUFFER,we),n.framebufferRenderbuffer(n.FRAMEBUFFER,de,n.RENDERBUFFER,we)}}else{let se=B.texture.mipmaps;if(se&&se.length>0?t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer[0]):t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer),E.__webglDepthbuffer===void 0)E.__webglDepthbuffer=n.createRenderbuffer(),Et(E.__webglDepthbuffer,B,!1);else{let de=B.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,we=E.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,we),n.framebufferRenderbuffer(n.FRAMEBUFFER,de,n.RENDERBUFFER,we)}}t.bindFramebuffer(n.FRAMEBUFFER,null)}function Ft(B,E,$){let se=i.get(B);E!==void 0&&Ge(se.__webglFramebuffer,B,B.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),$!==void 0&&bt(B)}function Wt(B){let E=B.texture,$=i.get(B),se=i.get(E);B.addEventListener("dispose",M);let de=B.textures,we=B.isWebGLCubeRenderTarget===!0,Ae=de.length>1;if(Ae||(se.__webglTexture===void 0&&(se.__webglTexture=n.createTexture()),se.__version=E.version,o.memory.textures++),we){$.__webglFramebuffer=[];for(let ce=0;ce<6;ce++)if(E.mipmaps&&E.mipmaps.length>0){$.__webglFramebuffer[ce]=[];for(let re=0;re<E.mipmaps.length;re++)$.__webglFramebuffer[ce][re]=n.createFramebuffer()}else $.__webglFramebuffer[ce]=n.createFramebuffer()}else{if(E.mipmaps&&E.mipmaps.length>0){$.__webglFramebuffer=[];for(let ce=0;ce<E.mipmaps.length;ce++)$.__webglFramebuffer[ce]=n.createFramebuffer()}else $.__webglFramebuffer=n.createFramebuffer();if(Ae)for(let ce=0,re=de.length;ce<re;ce++){let Ie=i.get(de[ce]);Ie.__webglTexture===void 0&&(Ie.__webglTexture=n.createTexture(),o.memory.textures++)}if(B.samples>0&&Rt(B)===!1){$.__webglMultisampledFramebuffer=n.createFramebuffer(),$.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,$.__webglMultisampledFramebuffer);for(let ce=0;ce<de.length;ce++){let re=de[ce];$.__webglColorRenderbuffer[ce]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,$.__webglColorRenderbuffer[ce]);let Ie=r.convert(re.format,re.colorSpace),Ze=r.convert(re.type),Fe=T(re.internalFormat,Ie,Ze,re.normalized,re.colorSpace,B.isXRRenderTarget===!0),Se=vt(B);n.renderbufferStorageMultisample(n.RENDERBUFFER,Se,Fe,B.width,B.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ce,n.RENDERBUFFER,$.__webglColorRenderbuffer[ce])}n.bindRenderbuffer(n.RENDERBUFFER,null),B.depthBuffer&&($.__webglDepthRenderbuffer=n.createRenderbuffer(),Et($.__webglDepthRenderbuffer,B,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(we){t.bindTexture(n.TEXTURE_CUBE_MAP,se.__webglTexture),et(n.TEXTURE_CUBE_MAP,E);for(let ce=0;ce<6;ce++)if(E.mipmaps&&E.mipmaps.length>0)for(let re=0;re<E.mipmaps.length;re++)Ge($.__webglFramebuffer[ce][re],B,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ce,re);else Ge($.__webglFramebuffer[ce],B,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ce,0);m(E)&&A(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ae){for(let ce=0,re=de.length;ce<re;ce++){let Ie=de[ce],Ze=i.get(Ie),Fe=n.TEXTURE_2D;(B.isWebGL3DRenderTarget||B.isWebGLArrayRenderTarget)&&(Fe=B.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(Fe,Ze.__webglTexture),et(Fe,Ie),Ge($.__webglFramebuffer,B,Ie,n.COLOR_ATTACHMENT0+ce,Fe,0),m(Ie)&&A(Fe)}t.unbindTexture()}else{let ce=n.TEXTURE_2D;if((B.isWebGL3DRenderTarget||B.isWebGLArrayRenderTarget)&&(ce=B.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ce,se.__webglTexture),et(ce,E),E.mipmaps&&E.mipmaps.length>0)for(let re=0;re<E.mipmaps.length;re++)Ge($.__webglFramebuffer[re],B,E,n.COLOR_ATTACHMENT0,ce,re);else Ge($.__webglFramebuffer,B,E,n.COLOR_ATTACHMENT0,ce,0);m(E)&&A(ce),t.unbindTexture()}B.depthBuffer&&bt(B)}function Tt(B){let E=B.textures;for(let $=0,se=E.length;$<se;$++){let de=E[$];if(m(de)){let we=U(B),Ae=i.get(de).__webglTexture;t.bindTexture(we,Ae),A(we),t.unbindTexture()}}}let Jt=[],bn=[];function xe(B){if(B.samples>0){if(Rt(B)===!1){let E=B.textures,$=B.width,se=B.height,de=n.COLOR_BUFFER_BIT,we=B.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Ae=i.get(B),ce=E.length>1;if(ce)for(let Ie=0;Ie<E.length;Ie++)t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ie,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ie,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer);let re=B.texture.mipmaps;re&&re.length>0?t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer[0]):t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer);for(let Ie=0;Ie<E.length;Ie++){if(B.resolveDepthBuffer&&(B.depthBuffer&&(de|=n.DEPTH_BUFFER_BIT),B.stencilBuffer&&B.resolveStencilBuffer&&(de|=n.STENCIL_BUFFER_BIT)),ce){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ie]);let Ze=i.get(E[Ie]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Ze,0)}n.blitFramebuffer(0,0,$,se,0,0,$,se,de,n.NEAREST),c===!0&&(Jt.length=0,bn.length=0,Jt.push(n.COLOR_ATTACHMENT0+Ie),B.depthBuffer&&B.storeMultisampledDepthBuffer===!1&&(Jt.push(we),bn.push(we),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,bn)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,Jt))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ce)for(let Ie=0;Ie<E.length;Ie++){t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ie,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ie]);let Ze=i.get(E[Ie]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ie,n.TEXTURE_2D,Ze,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer)}else if(B.depthBuffer&&B.storeMultisampledDepthBuffer===!1&&c){let E=B.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[E])}}}function vt(B){return Math.min(s.maxSamples,B.samples)}function Rt(B){let E=i.get(B);return B.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&E.__useRenderToTexture!==!1}function X(B){let E=o.render.frame;u.get(B)!==E&&(u.set(B,E),B.update())}function xn(B,E){let $=B.colorSpace,se=B.format,de=B.type;return B.isCompressedTexture===!0||B.isVideoTexture===!0||$!==ti&&$!==$s&&(It.getTransfer($)===Gt?(se!==Si||de!==di)&&nt("WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):ht("WebGLTextures: Unsupported texture color space:",$)),E}function lt(B){return typeof HTMLImageElement<"u"&&B instanceof HTMLImageElement?(l.width=B.naturalWidth||B.width,l.height=B.naturalHeight||B.height):typeof VideoFrame<"u"&&B instanceof VideoFrame?(l.width=B.displayWidth,l.height=B.displayHeight):(l.width=B.width,l.height=B.height),l}this.allocateTextureUnit=he,this.resetTextureUnits=q,this.getTextureUnits=z,this.setTextureUnits=ee,this.setTexture2D=ye,this.setTexture2DArray=V,this.setTexture3D=Q,this.setTextureCube=le,this.rebindTextures=Ft,this.setupRenderTarget=Wt,this.updateRenderTargetMipmap=Tt,this.updateMultisampleRenderTarget=xe,this.setupDepthRenderbuffer=bt,this.setupFrameBufferTexture=Ge,this.useMultisampledRTT=Rt,this.isReversedDepthBuffer=function(){return t.buffers.depth.getReversed()}}function GE(n,e){function t(i,s=$s){let r,o=It.getTransfer(s);if(i===di)return n.UNSIGNED_BYTE;if(i===Mh)return n.UNSIGNED_SHORT_4_4_4_4;if(i===Eh)return n.UNSIGNED_SHORT_5_5_5_1;if(i===kd)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===Vd)return n.UNSIGNED_INT_10F_11F_11F_REV;if(i===Bd)return n.BYTE;if(i===Hd)return n.SHORT;if(i===la)return n.UNSIGNED_SHORT;if(i===yh)return n.INT;if(i===ss)return n.UNSIGNED_INT;if(i===Ti)return n.FLOAT;if(i===rs)return n.HALF_FLOAT;if(i===zd)return n.ALPHA;if(i===Gd)return n.RGB;if(i===Si)return n.RGBA;if(i===xs)return n.DEPTH_COMPONENT;if(i===_r)return n.DEPTH_STENCIL;if(i===bh)return n.RED;if(i===Th)return n.RED_INTEGER;if(i===xr)return n.RG;if(i===Sh)return n.RG_INTEGER;if(i===wh)return n.RGBA_INTEGER;if(i===bl||i===Tl||i===Sl||i===wl)if(o===Gt)if(r=e.get("WEBGL_compressed_texture_s3tc_srgb"),r!==null){if(i===bl)return r.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Tl)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Sl)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===wl)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(r=e.get("WEBGL_compressed_texture_s3tc"),r!==null){if(i===bl)return r.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Tl)return r.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Sl)return r.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===wl)return r.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===Ah||i===Rh||i===Ch||i===Ih)if(r=e.get("WEBGL_compressed_texture_pvrtc"),r!==null){if(i===Ah)return r.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Rh)return r.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===Ch)return r.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===Ih)return r.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===Ph||i===Lh||i===Dh||i===Nh||i===Uh||i===Al||i===Fh)if(r=e.get("WEBGL_compressed_texture_etc"),r!==null){if(i===Ph||i===Lh)return o===Gt?r.COMPRESSED_SRGB8_ETC2:r.COMPRESSED_RGB8_ETC2;if(i===Dh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:r.COMPRESSED_RGBA8_ETC2_EAC;if(i===Nh)return r.COMPRESSED_R11_EAC;if(i===Uh)return r.COMPRESSED_SIGNED_R11_EAC;if(i===Al)return r.COMPRESSED_RG11_EAC;if(i===Fh)return r.COMPRESSED_SIGNED_RG11_EAC}else return null;if(i===Oh||i===Bh||i===Hh||i===kh||i===Vh||i===zh||i===Gh||i===Wh||i===Xh||i===qh||i===Yh||i===$h||i===Zh||i===Kh)if(r=e.get("WEBGL_compressed_texture_astc"),r!==null){if(i===Oh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:r.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===Bh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:r.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===Hh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:r.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===kh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:r.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===Vh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:r.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===zh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:r.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===Gh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:r.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===Wh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:r.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===Xh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:r.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===qh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:r.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===Yh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:r.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===$h)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:r.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===Zh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:r.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===Kh)return o===Gt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:r.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===jh||i===Jh||i===Qh)if(r=e.get("EXT_texture_compression_bptc"),r!==null){if(i===jh)return o===Gt?r.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:r.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===Jh)return r.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===Qh)return r.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===eu||i===tu||i===Rl||i===nu)if(r=e.get("EXT_texture_compression_rgtc"),r!==null){if(i===eu)return r.COMPRESSED_RED_RGTC1_EXT;if(i===tu)return r.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===Rl)return r.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===nu)return r.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===ca?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}var WE=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,XE=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`,ff=class{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t){if(this.texture===null){let i=new rl(e.texture);(e.depthNear!==t.depthNear||e.depthFar!==t.depthFar)&&(this.depthNear=e.depthNear,this.depthFar=e.depthFar),this.texture=i}}getMesh(e){if(this.texture!==null&&this.mesh===null){let t=e.cameras[0].viewport,i=new Un({vertexShader:WE,fragmentShader:XE,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new dn(new cn(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}},pf=class extends Qi{constructor(e,t){super();let i=this,s=null,r=1,o=null,a="local-floor",c=1,l=null,u=null,d=null,f=null,p=null,x=null,b=typeof XRWebGLBinding<"u",g=new ff,m={},A=t.getContextAttributes(),U=null,T=null,I=[],L=[],P=new Pe,M=null,C=null,O=new An;O.viewport=new $t;let H=new An;H.viewport=new $t;let k=[O,H],q=new mh,z=null,ee=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(ae){let me=I[ae];return me===void 0&&(me=new Ko,I[ae]=me),me.getTargetRaySpace()},this.getControllerGrip=function(ae){let me=I[ae];return me===void 0&&(me=new Ko,I[ae]=me),me.getGripSpace()},this.getHand=function(ae){let me=I[ae];return me===void 0&&(me=new Ko,I[ae]=me),me.getHandSpace()};function he(ae){let me=L.indexOf(ae.inputSource);if(me===-1)return;let qe=I[me];qe!==void 0&&(qe.update(ae.inputSource,ae.frame,l||o),qe.dispatchEvent({type:ae.type,data:ae.inputSource}))}function ue(){s.removeEventListener("select",he),s.removeEventListener("selectstart",he),s.removeEventListener("selectend",he),s.removeEventListener("squeeze",he),s.removeEventListener("squeezestart",he),s.removeEventListener("squeezeend",he),s.removeEventListener("end",ue),s.removeEventListener("inputsourceschange",ye);for(let ae=0;ae<I.length;ae++){let me=L[ae];me!==null&&(L[ae]=null,I[ae].disconnect(me))}z=null,ee=null,g.reset();for(let ae in m)delete m[ae];if(e.setRenderTarget(U),p=null,f=null,d=null,s=null,T=null,ct.stop(),i.isPresenting=!1,e.setPixelRatio(M),e.setSize(P.width,P.height,!1),C!==null){let ae=C.camera;ae.fov=C.fov,ae.zoom=C.zoom,ae.updateProjectionMatrix(),C=null}i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(ae){r=ae,i.isPresenting===!0&&nt("WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(ae){a=ae,i.isPresenting===!0&&nt("WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||o},this.setReferenceSpace=function(ae){l=ae},this.getBaseLayer=function(){return f!==null?f:p},this.getBinding=function(){return d===null&&b&&(d=new XRWebGLBinding(s,t)),d},this.getFrame=function(){return x},this.getSession=function(){return s},this.setSession=async function(ae){if(s=ae,s!==null){if(U=e.getRenderTarget(),s.addEventListener("select",he),s.addEventListener("selectstart",he),s.addEventListener("selectend",he),s.addEventListener("squeeze",he),s.addEventListener("squeezestart",he),s.addEventListener("squeezeend",he),s.addEventListener("end",ue),s.addEventListener("inputsourceschange",ye),A.xrCompatible!==!0&&await t.makeXRCompatible(),M=e.getPixelRatio(),e.getSize(P),b&&"createProjectionLayer"in XRWebGLBinding.prototype){let qe=null,ft=null,Ge=null;A.depth&&(Ge=A.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,qe=A.stencil?_r:xs,ft=A.stencil?ca:ss);let Et={colorFormat:t.RGBA8,depthFormat:Ge,scaleFactor:r};d=this.getBinding(),f=d.createProjectionLayer(Et),s.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),T=new ai(f.textureWidth,f.textureHeight,{format:Si,type:di,depthTexture:new dr(f.textureWidth,f.textureHeight,ft,void 0,void 0,void 0,void 0,void 0,void 0,qe),stencilBuffer:A.stencil,colorSpace:e.outputColorSpace,samples:A.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1,storeMultisampledDepthBuffer:f.ignoreDepthValues===!1,storeMultisampledStencilBuffer:f.ignoreDepthValues===!1})}else{let qe={antialias:A.antialias,alpha:!0,depth:A.depth,stencil:A.stencil,framebufferScaleFactor:r};p=new XRWebGLLayer(s,t,qe),s.updateRenderState({baseLayer:p}),e.setPixelRatio(1),e.setSize(p.framebufferWidth,p.framebufferHeight,!1),T=new ai(p.framebufferWidth,p.framebufferHeight,{format:Si,type:di,colorSpace:e.outputColorSpace,stencilBuffer:A.stencil,resolveDepthBuffer:p.ignoreDepthValues===!1,resolveStencilBuffer:p.ignoreDepthValues===!1,storeMultisampledDepthBuffer:p.ignoreDepthValues===!1,storeMultisampledStencilBuffer:p.ignoreDepthValues===!1})}T.isXRRenderTarget=!0,this.setFoveation(c),l=null,o=await s.requestReferenceSpace(a),ct.setContext(s),ct.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(s!==null)return s.environmentBlendMode},this.getDepthTexture=function(){return g.getDepthTexture()};function ye(ae){for(let me=0;me<ae.removed.length;me++){let qe=ae.removed[me],ft=L.indexOf(qe);ft>=0&&(L[ft]=null,I[ft].disconnect(qe))}for(let me=0;me<ae.added.length;me++){let qe=ae.added[me],ft=L.indexOf(qe);if(ft===-1){for(let Et=0;Et<I.length;Et++)if(Et>=L.length){L.push(qe),ft=Et;break}else if(L[Et]===null){L[Et]=qe,ft=Et;break}if(ft===-1)break}let Ge=I[ft];Ge&&Ge.connect(qe)}}let V=new y,Q=new y;function le(ae,me,qe){V.setFromMatrixPosition(me.matrixWorld),Q.setFromMatrixPosition(qe.matrixWorld);let ft=V.distanceTo(Q),Ge=me.projectionMatrix.elements,Et=qe.projectionMatrix.elements,pn=Ge[14]/(Ge[10]-1),bt=Ge[14]/(Ge[10]+1),Ft=(Ge[9]+1)/Ge[5],Wt=(Ge[9]-1)/Ge[5],Tt=(Ge[8]-1)/Ge[0],Jt=(Et[8]+1)/Et[0],bn=pn*Tt,xe=pn*Jt,vt=ft/(-Tt+Jt),Rt=vt*-Tt;if(me.matrixWorld.decompose(ae.position,ae.quaternion,ae.scale),ae.translateX(Rt),ae.translateZ(vt),ae.matrixWorld.compose(ae.position,ae.quaternion,ae.scale),ae.matrixWorldInverse.copy(ae.matrixWorld).invert(),Ge[10]===-1)ae.projectionMatrix.copy(me.projectionMatrix),ae.projectionMatrixInverse.copy(me.projectionMatrixInverse);else{let X=pn+vt,xn=bt+vt,lt=bn-Rt,B=xe+(ft-Rt),E=Ft*bt/xn*X,$=Wt*bt/xn*X;ae.projectionMatrix.makePerspective(lt,B,E,$,X,xn),ae.projectionMatrixInverse.copy(ae.projectionMatrix).invert()}}function Ee(ae,me){me===null?ae.matrixWorld.copy(ae.matrix):ae.matrixWorld.multiplyMatrices(me.matrixWorld,ae.matrix),ae.matrixWorldInverse.copy(ae.matrixWorld).invert()}this.updateCamera=function(ae){if(s===null)return;let me=ae.near,qe=ae.far;g.texture!==null&&(g.depthNear>0&&(me=g.depthNear),g.depthFar>0&&(qe=g.depthFar)),q.near=H.near=O.near=me,q.far=H.far=O.far=qe,(z!==q.near||ee!==q.far)&&(s.updateRenderState({depthNear:q.near,depthFar:q.far}),z=q.near,ee=q.far),q.layers.mask=ae.layers.mask|6,O.layers.mask=q.layers.mask&-5,H.layers.mask=q.layers.mask&-3;let ft=ae.parent,Ge=q.cameras;Ee(q,ft);for(let Et=0;Et<Ge.length;Et++)Ee(Ge[Et],ft);Ge.length===2?le(q,O,H):q.projectionMatrix.copy(O.projectionMatrix),C===null&&ae.isPerspectiveCamera&&(C={camera:ae,fov:ae.fov,zoom:ae.zoom}),be(ae,q,ft)};function be(ae,me,qe){qe===null?ae.matrix.copy(me.matrixWorld):(ae.matrix.copy(qe.matrixWorld),ae.matrix.invert(),ae.matrix.multiply(me.matrixWorld)),ae.matrix.decompose(ae.position,ae.quaternion,ae.scale),ae.updateMatrixWorld(!0),ae.projectionMatrix.copy(me.projectionMatrix),ae.projectionMatrixInverse.copy(me.projectionMatrixInverse),ae.isPerspectiveCamera&&(ae.fov=Gr*2*Math.atan(1/ae.projectionMatrix.elements[5]),ae.zoom=1)}this.getCamera=function(){return q},this.getFoveation=function(){if(!(f===null&&p===null))return c},this.setFoveation=function(ae){c=ae,f!==null&&(f.fixedFoveation=ae),p!==null&&p.fixedFoveation!==void 0&&(p.fixedFoveation=ae)},this.hasDepthSensing=function(){return g.texture!==null},this.getDepthSensingMesh=function(){return g.getMesh(q)},this.getCameraTexture=function(ae){return m[ae]};let ut=null;function et(ae,me){if(u=me.getViewerPose(l||o),x=me,u!==null){let qe=u.views;p!==null&&(e.setRenderTargetFramebuffer(T,p.framebuffer),e.setRenderTarget(T));let ft=!1;qe.length!==q.cameras.length&&(q.cameras.length=0,ft=!0);for(let bt=0;bt<qe.length;bt++){let Ft=qe[bt],Wt=null;if(p!==null)Wt=p.getViewport(Ft);else{let Jt=d.getViewSubImage(f,Ft);Wt=Jt.viewport,bt===0&&(e.setRenderTargetTextures(T,Jt.colorTexture,Jt.depthStencilTexture),e.setRenderTarget(T))}let Tt=k[bt];Tt===void 0&&(Tt=new An,Tt.layers.enable(bt),Tt.viewport=new $t,k[bt]=Tt),Tt.matrix.fromArray(Ft.transform.matrix),Tt.matrix.decompose(Tt.position,Tt.quaternion,Tt.scale),Tt.projectionMatrix.fromArray(Ft.projectionMatrix),Tt.projectionMatrixInverse.copy(Tt.projectionMatrix).invert(),Tt.viewport.set(Wt.x,Wt.y,Wt.width,Wt.height),bt===0&&(q.matrix.copy(Tt.matrix),q.matrix.decompose(q.position,q.quaternion,q.scale)),ft===!0&&q.cameras.push(Tt)}let Ge=s.enabledFeatures;if(Ge&&Ge.includes("depth-sensing")&&s.depthUsage=="gpu-optimized"&&b){d=i.getBinding();let bt=d.getDepthInformation(qe[0]);bt&&bt.isValid&&bt.texture&&g.init(bt,s.renderState)}if(Ge&&Ge.includes("camera-access")&&b){e.state.unbindTexture(),d=i.getBinding();for(let bt=0;bt<qe.length;bt++){let Ft=qe[bt].camera;if(Ft){let Wt=m[Ft];Wt||(Wt=new rl,m[Ft]=Wt);let Tt=d.getCameraImage(Ft);Wt.sourceTexture=Tt}}}}for(let qe=0;qe<I.length;qe++){let ft=L[qe],Ge=I[qe];ft!==null&&Ge!==void 0&&Ge.update(ft,me,l||o)}ut&&ut(ae,me),me.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:me}),x=null}let ct=new I0;ct.setAnimationLoop(et),this.setAnimationLoop=function(ae){ut=ae},this.dispose=function(){}}},qE=new rt,F0=new gt;F0.set(-1,0,0,0,1,0,0,0,1);function YE(n,e){function t(g,m){g.matrixAutoUpdate===!0&&g.updateMatrix(),m.value.copy(g.matrix)}function i(g,m){m.color.getRGB(g.fogColor.value,Zd(n)),m.isFog?(g.fogNear.value=m.near,g.fogFar.value=m.far):m.isFogExp2&&(g.fogDensity.value=m.density)}function s(g,m,A,U,T){m.isNodeMaterial?m.uniformsNeedUpdate=!1:m.isMeshBasicMaterial?r(g,m):m.isMeshLambertMaterial?(r(g,m),m.envMap&&(g.envMapIntensity.value=m.envMapIntensity)):m.isMeshToonMaterial?(r(g,m),d(g,m)):m.isMeshPhongMaterial?(r(g,m),u(g,m),m.envMap&&(g.envMapIntensity.value=m.envMapIntensity)):m.isMeshStandardMaterial?(r(g,m),f(g,m),m.isMeshPhysicalMaterial&&p(g,m,T)):m.isMeshMatcapMaterial?(r(g,m),x(g,m)):m.isMeshDepthMaterial?r(g,m):m.isMeshDistanceMaterial?(r(g,m),b(g,m)):m.isMeshNormalMaterial?r(g,m):m.isLineBasicMaterial?(o(g,m),m.isLineDashedMaterial&&a(g,m)):m.isPointsMaterial?c(g,m,A,U):m.isSpriteMaterial?l(g,m):m.isShadowMaterial?(g.color.value.copy(m.color),g.opacity.value=m.opacity):m.isShaderMaterial&&(m.uniformsNeedUpdate=!1)}function r(g,m){g.opacity.value=m.opacity,m.color&&g.diffuse.value.copy(m.color),m.emissive&&g.emissive.value.copy(m.emissive).multiplyScalar(m.emissiveIntensity),m.map&&(g.map.value=m.map,t(m.map,g.mapTransform)),m.alphaMap&&(g.alphaMap.value=m.alphaMap,t(m.alphaMap,g.alphaMapTransform)),m.bumpMap&&(g.bumpMap.value=m.bumpMap,t(m.bumpMap,g.bumpMapTransform),g.bumpScale.value=m.bumpScale,m.side===Hn&&(g.bumpScale.value*=-1)),m.normalMap&&(g.normalMap.value=m.normalMap,t(m.normalMap,g.normalMapTransform),g.normalScale.value.copy(m.normalScale),m.side===Hn&&g.normalScale.value.negate()),m.displacementMap&&(g.displacementMap.value=m.displacementMap,t(m.displacementMap,g.displacementMapTransform),g.displacementScale.value=m.displacementScale,g.displacementBias.value=m.displacementBias),m.emissiveMap&&(g.emissiveMap.value=m.emissiveMap,t(m.emissiveMap,g.emissiveMapTransform)),m.specularMap&&(g.specularMap.value=m.specularMap,t(m.specularMap,g.specularMapTransform)),m.alphaTest>0&&(g.alphaTest.value=m.alphaTest);let A=e.get(m),U=A.envMap,T=A.envMapRotation;U&&(g.envMap.value=U,g.envMapRotation.value.setFromMatrix4(qE.makeRotationFromEuler(T)).transpose(),U.isCubeTexture&&U.isRenderTargetTexture===!1&&g.envMapRotation.value.premultiply(F0),g.reflectivity.value=m.reflectivity,g.ior.value=m.ior,g.refractionRatio.value=m.refractionRatio),m.lightMap&&(g.lightMap.value=m.lightMap,g.lightMapIntensity.value=m.lightMapIntensity,t(m.lightMap,g.lightMapTransform)),m.aoMap&&(g.aoMap.value=m.aoMap,g.aoMapIntensity.value=m.aoMapIntensity,t(m.aoMap,g.aoMapTransform))}function o(g,m){g.diffuse.value.copy(m.color),g.opacity.value=m.opacity,m.map&&(g.map.value=m.map,t(m.map,g.mapTransform))}function a(g,m){g.dashSize.value=m.dashSize,g.totalSize.value=m.dashSize+m.gapSize,g.scale.value=m.scale}function c(g,m,A,U){g.diffuse.value.copy(m.color),g.opacity.value=m.opacity,g.size.value=m.size*A,g.scale.value=U*.5,m.map&&(g.map.value=m.map,t(m.map,g.uvTransform)),m.alphaMap&&(g.alphaMap.value=m.alphaMap,t(m.alphaMap,g.alphaMapTransform)),m.alphaTest>0&&(g.alphaTest.value=m.alphaTest)}function l(g,m){g.diffuse.value.copy(m.color),g.opacity.value=m.opacity,g.rotation.value=m.rotation,m.map&&(g.map.value=m.map,t(m.map,g.mapTransform)),m.alphaMap&&(g.alphaMap.value=m.alphaMap,t(m.alphaMap,g.alphaMapTransform)),m.alphaTest>0&&(g.alphaTest.value=m.alphaTest)}function u(g,m){g.specular.value.copy(m.specular),g.shininess.value=Math.max(m.shininess,1e-4)}function d(g,m){m.gradientMap&&(g.gradientMap.value=m.gradientMap)}function f(g,m){g.metalness.value=m.metalness,m.metalnessMap&&(g.metalnessMap.value=m.metalnessMap,t(m.metalnessMap,g.metalnessMapTransform)),g.roughness.value=m.roughness,m.roughnessMap&&(g.roughnessMap.value=m.roughnessMap,t(m.roughnessMap,g.roughnessMapTransform)),m.envMap&&(g.envMapIntensity.value=m.envMapIntensity)}function p(g,m,A){g.ior.value=m.ior,m.sheen>0&&(g.sheenColor.value.copy(m.sheenColor).multiplyScalar(m.sheen),g.sheenRoughness.value=m.sheenRoughness,m.sheenColorMap&&(g.sheenColorMap.value=m.sheenColorMap,t(m.sheenColorMap,g.sheenColorMapTransform)),m.sheenRoughnessMap&&(g.sheenRoughnessMap.value=m.sheenRoughnessMap,t(m.sheenRoughnessMap,g.sheenRoughnessMapTransform))),m.clearcoat>0&&(g.clearcoat.value=m.clearcoat,g.clearcoatRoughness.value=m.clearcoatRoughness,m.clearcoatMap&&(g.clearcoatMap.value=m.clearcoatMap,t(m.clearcoatMap,g.clearcoatMapTransform)),m.clearcoatRoughnessMap&&(g.clearcoatRoughnessMap.value=m.clearcoatRoughnessMap,t(m.clearcoatRoughnessMap,g.clearcoatRoughnessMapTransform)),m.clearcoatNormalMap&&(g.clearcoatNormalMap.value=m.clearcoatNormalMap,t(m.clearcoatNormalMap,g.clearcoatNormalMapTransform),g.clearcoatNormalScale.value.copy(m.clearcoatNormalScale),m.side===Hn&&g.clearcoatNormalScale.value.negate())),m.dispersion>0&&(g.dispersion.value=m.dispersion),m.retroreflectivity>0&&(g.retroreflectivity.value=m.retroreflectivity),m.iridescence>0&&(g.iridescence.value=m.iridescence,g.iridescenceIOR.value=m.iridescenceIOR,g.iridescenceThicknessMinimum.value=m.iridescenceThicknessRange[0],g.iridescenceThicknessMaximum.value=m.iridescenceThicknessRange[1],m.iridescenceMap&&(g.iridescenceMap.value=m.iridescenceMap,t(m.iridescenceMap,g.iridescenceMapTransform)),m.iridescenceThicknessMap&&(g.iridescenceThicknessMap.value=m.iridescenceThicknessMap,t(m.iridescenceThicknessMap,g.iridescenceThicknessMapTransform))),m.transmission>0&&(g.transmission.value=m.transmission,g.transmissionSamplerMap.value=A.texture,g.transmissionSamplerSize.value.set(A.width,A.height),m.transmissionMap&&(g.transmissionMap.value=m.transmissionMap,t(m.transmissionMap,g.transmissionMapTransform)),g.thickness.value=m.thickness,m.thicknessMap&&(g.thicknessMap.value=m.thicknessMap,t(m.thicknessMap,g.thicknessMapTransform)),g.attenuationDistance.value=m.attenuationDistance,g.attenuationColor.value.copy(m.attenuationColor)),m.anisotropy>0&&(g.anisotropyVector.value.set(m.anisotropy*Math.cos(m.anisotropyRotation),m.anisotropy*Math.sin(m.anisotropyRotation)),m.anisotropyMap&&(g.anisotropyMap.value=m.anisotropyMap,t(m.anisotropyMap,g.anisotropyMapTransform))),g.specularIntensity.value=m.specularIntensity,g.specularColor.value.copy(m.specularColor),m.specularColorMap&&(g.specularColorMap.value=m.specularColorMap,t(m.specularColorMap,g.specularColorMapTransform)),m.specularIntensityMap&&(g.specularIntensityMap.value=m.specularIntensityMap,t(m.specularIntensityMap,g.specularIntensityMapTransform))}function x(g,m){m.matcap&&(g.matcap.value=m.matcap)}function b(g,m){let A=e.get(m).light;g.referencePosition.value.setFromMatrixPosition(A.matrixWorld),g.nearDistance.value=A.shadow.camera.near,g.farDistance.value=A.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:s}}function $E(n,e,t,i){let s={},r={},o=[],a=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(T,I){let L=I.program;i.uniformBlockBinding(T,L)}function l(T,I){let L=s[T.id];L===void 0&&(g(T),L=u(T),s[T.id]=L,T.addEventListener("dispose",A));let P=I.program;i.updateUBOMapping(T,P);let M=e.render.frame;r[T.id]!==M&&(f(T),r[T.id]=M)}function u(T){let I=d();T.__bindingPointIndex=I;let L=n.createBuffer(),P=T.__size,M=T.usage;return n.bindBuffer(n.UNIFORM_BUFFER,L),n.bufferData(n.UNIFORM_BUFFER,P,M),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,I,L),L}function d(){for(let T=0;T<a;T++)if(o.indexOf(T)===-1)return o.push(T),T;return ht("WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(T){let I=s[T.id],L=T.uniforms,P=T.__cache;n.bindBuffer(n.UNIFORM_BUFFER,I);for(let M=0,C=L.length;M<C;M++){let O=L[M];if(Array.isArray(O))for(let H=0,k=O.length;H<k;H++)p(O[H],M,H,P);else p(O,M,0,P)}n.bindBuffer(n.UNIFORM_BUFFER,null)}function p(T,I,L,P){if(b(T,I,L,P)===!0){let M=T.__offset,C=T.value;if(Array.isArray(C)){let O=0;for(let H=0;H<C.length;H++){let k=C[H],q=m(k);x(k,T.__data,O),typeof k!="number"&&typeof k!="boolean"&&!k.isMatrix3&&!ArrayBuffer.isView(k)&&(O+=q.storage/Float32Array.BYTES_PER_ELEMENT)}}else x(C,T.__data,0);n.bufferSubData(n.UNIFORM_BUFFER,M,T.__data)}}function x(T,I,L){typeof T=="number"||typeof T=="boolean"?I[0]=T:T.isMatrix3?(I[0]=T.elements[0],I[1]=T.elements[1],I[2]=T.elements[2],I[3]=0,I[4]=T.elements[3],I[5]=T.elements[4],I[6]=T.elements[5],I[7]=0,I[8]=T.elements[6],I[9]=T.elements[7],I[10]=T.elements[8],I[11]=0):ArrayBuffer.isView(T)?I.set(new T.constructor(T.buffer,T.byteOffset,I.length)):T.toArray(I,L)}function b(T,I,L,P){let M=T.value,C=I+"_"+L;if(P[C]===void 0)return typeof M=="number"||typeof M=="boolean"?P[C]=M:ArrayBuffer.isView(M)?P[C]=M.slice():P[C]=M.clone(),!0;{let O=P[C];if(typeof M=="number"||typeof M=="boolean"){if(O!==M)return P[C]=M,!0}else{if(ArrayBuffer.isView(M))return!0;if(O.equals(M)===!1)return O.copy(M),!0}}return!1}function g(T){let I=T.uniforms,L=0,P=16;for(let C=0,O=I.length;C<O;C++){let H=Array.isArray(I[C])?I[C]:[I[C]];for(let k=0,q=H.length;k<q;k++){let z=H[k],ee=Array.isArray(z.value)?z.value:[z.value];for(let he=0,ue=ee.length;he<ue;he++){let ye=ee[he],V=m(ye),Q=L%P,le=Q%V.boundary,Ee=Q+le;L+=le,Ee!==0&&P-Ee<V.storage&&(L+=P-Ee),z.__data=new Float32Array(V.storage/Float32Array.BYTES_PER_ELEMENT),z.__offset=L,L+=V.storage}}}let M=L%P;return M>0&&(L+=P-M),T.__size=L,T.__cache={},this}function m(T){let I={boundary:0,storage:0};return typeof T=="number"||typeof T=="boolean"?(I.boundary=4,I.storage=4):T.isVector2?(I.boundary=8,I.storage=8):T.isVector3||T.isColor?(I.boundary=16,I.storage=12):T.isVector4?(I.boundary=16,I.storage=16):T.isMatrix3?(I.boundary=48,I.storage=48):T.isMatrix4?(I.boundary=64,I.storage=64):T.isTexture?nt("WebGLRenderer: Texture samplers can not be part of an uniforms group."):ArrayBuffer.isView(T)?(I.boundary=16,I.storage=T.byteLength):nt("WebGLRenderer: Unsupported uniform value type.",T),I}function A(T){let I=T.target;I.removeEventListener("dispose",A);let L=o.indexOf(I.__bindingPointIndex);o.splice(L,1),n.deleteBuffer(s[I.id]),delete s[I.id],delete r[I.id]}function U(){for(let T in s)n.deleteBuffer(s[T]);o=[],s={},r={}}return{bind:c,update:l,dispose:U}}var ZE=new Uint16Array([12469,15057,12620,14925,13266,14620,13807,14376,14323,13990,14545,13625,14713,13328,14840,12882,14931,12528,14996,12233,15039,11829,15066,11525,15080,11295,15085,10976,15082,10705,15073,10495,13880,14564,13898,14542,13977,14430,14158,14124,14393,13732,14556,13410,14702,12996,14814,12596,14891,12291,14937,11834,14957,11489,14958,11194,14943,10803,14921,10506,14893,10278,14858,9960,14484,14039,14487,14025,14499,13941,14524,13740,14574,13468,14654,13106,14743,12678,14818,12344,14867,11893,14889,11509,14893,11180,14881,10751,14852,10428,14812,10128,14765,9754,14712,9466,14764,13480,14764,13475,14766,13440,14766,13347,14769,13070,14786,12713,14816,12387,14844,11957,14860,11549,14868,11215,14855,10751,14825,10403,14782,10044,14729,9651,14666,9352,14599,9029,14967,12835,14966,12831,14963,12804,14954,12723,14936,12564,14917,12347,14900,11958,14886,11569,14878,11247,14859,10765,14828,10401,14784,10011,14727,9600,14660,9289,14586,8893,14508,8533,15111,12234,15110,12234,15104,12216,15092,12156,15067,12010,15028,11776,14981,11500,14942,11205,14902,10752,14861,10393,14812,9991,14752,9570,14682,9252,14603,8808,14519,8445,14431,8145,15209,11449,15208,11451,15202,11451,15190,11438,15163,11384,15117,11274,15055,10979,14994,10648,14932,10343,14871,9936,14803,9532,14729,9218,14645,8742,14556,8381,14461,8020,14365,7603,15273,10603,15272,10607,15267,10619,15256,10631,15231,10614,15182,10535,15118,10389,15042,10167,14963,9787,14883,9447,14800,9115,14710,8665,14615,8318,14514,7911,14411,7507,14279,7198,15314,9675,15313,9683,15309,9712,15298,9759,15277,9797,15229,9773,15166,9668,15084,9487,14995,9274,14898,8910,14800,8539,14697,8234,14590,7790,14479,7409,14367,7067,14178,6621,15337,8619,15337,8631,15333,8677,15325,8769,15305,8871,15264,8940,15202,8909,15119,8775,15022,8565,14916,8328,14804,8009,14688,7614,14569,7287,14448,6888,14321,6483,14088,6171,15350,7402,15350,7419,15347,7480,15340,7613,15322,7804,15287,7973,15229,8057,15148,8012,15046,7846,14933,7611,14810,7357,14682,7069,14552,6656,14421,6316,14251,5948,14007,5528,15356,5942,15356,5977,15353,6119,15348,6294,15332,6551,15302,6824,15249,7044,15171,7122,15070,7050,14949,6861,14818,6611,14679,6349,14538,6067,14398,5651,14189,5311,13935,4958,15359,4123,15359,4153,15356,4296,15353,4646,15338,5160,15311,5508,15263,5829,15188,6042,15088,6094,14966,6001,14826,5796,14678,5543,14527,5287,14377,4985,14133,4586,13869,4257,15360,1563,15360,1642,15358,2076,15354,2636,15341,3350,15317,4019,15273,4429,15203,4732,15105,4911,14981,4932,14836,4818,14679,4621,14517,4386,14359,4156,14083,3795,13808,3437,15360,122,15360,137,15358,285,15355,636,15344,1274,15322,2177,15281,2765,15215,3223,15120,3451,14995,3569,14846,3567,14681,3466,14511,3305,14344,3121,14037,2800,13753,2467,15360,0,15360,1,15359,21,15355,89,15346,253,15325,479,15287,796,15225,1148,15133,1492,15008,1749,14856,1882,14685,1886,14506,1783,14324,1608,13996,1398,13702,1183]),Ts=null;function KE(){return Ts===null&&(Ts=new Qo(ZE,16,16,xr,rs),Ts.name="DFG_LUT",Ts.minFilter=yn,Ts.magFilter=yn,Ts.wrapS=Ii,Ts.wrapT=Ii,Ts.generateMipmaps=!1,Ts.needsUpdate=!0),Ts}var hu=class{constructor(e={}){let{canvas:t=t0(),context:i=null,depth:s=!0,stencil:r=!1,alpha:o=!1,antialias:a=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:u="default",failIfMajorPerformanceCaveat:d=!1,reversedDepthBuffer:f=!1,outputBufferType:p=di}=e;this.isWebGLRenderer=!0;let x;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");x=i.getContextAttributes().alpha}else x=o;let b=p,g=new Set([wh,Sh,Th]),m=new Set([di,ss,la,ca,Mh,Eh]),A=new Uint32Array(4),U=new Int32Array(4),T=new y,I=null,L=null,P=[],M=[],C=null;this.domElement=t,this.debug={checkShaderErrors:!0,diagnostics:{keywords:!1},onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=ns,this.toneMappingExposure=1,this.transmissionResolutionScale=1;let O=this,H=!1,k=null,q=null,z=null,ee=null;this._outputColorSpace=sn;let he=0,ue=0,ye=null,V=-1,Q=null,le=new $t,Ee=new $t,be=null,ut=new ke(0),et=0,ct=t.width,ae=t.height,me=1,qe=null,ft=null,Ge=new $t(0,0,ct,ae),Et=new $t(0,0,ct,ae),pn=!1,bt=new ea,Ft=!1,Wt=!1,Tt=new rt,Jt=new y,bn=new $t,xe={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0},vt=!1;function Rt(){return ye===null?me:1}let X=i;function xn(R,G){return t.getContext(R,G)}let lt,B,E,$,se,de,we,Ae,ce,re,Ie,Ze,Fe,Se,it,ot,xt,W,Te,oe,Re,He,ve;try{let R={alpha:!0,depth:s,stencil:r,antialias:a,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:u,failIfMajorPerformanceCaveat:d};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${"186"}`),t.addEventListener("webglcontextlost",Xt,!1),t.addEventListener("webglcontextrestored",De,!1),t.addEventListener("webglcontextcreationerror",On,!1),X===null){let G="webgl2";if(X=xn(G,R),X===null)throw xn(G)?new Error("THREE.WebGLRenderer: Error creating WebGL context with your selected attributes."):new Error("THREE.WebGLRenderer: Error creating WebGL context.")}st()}catch(R){throw t.removeEventListener("webglcontextlost",Xt,!1),t.removeEventListener("webglcontextrestored",De,!1),t.removeEventListener("webglcontextcreationerror",On,!1),ht("WebGLRenderer: "+R.message),R}function st(){lt=new iM(X),lt.init(),Re=new GE(X,lt),B=new Yy(X,lt,e,Re),E=new VE(X,lt),B.reversedDepthBuffer&&f&&E.buffers.depth.setReversed(!0),q=X.createFramebuffer(),z=X.createFramebuffer(),ee=X.createFramebuffer(),$=new oM(X),se=new AE,de=new zE(X,lt,E,se,B,Re,$),we=new nM(O),Ae=new lx(X),He=new Xy(X,Ae),ce=new sM(X,Ae,$,He),re=new lM(X,ce,Ae,He,$),W=new aM(X,B,de),it=new $y(se),Ie=new wE(O,we,lt,B,He,it),Ze=new YE(O,se),Fe=new CE,Se=new UE(lt),xt=new Wy(O,we,E,re,x,c),ot=new kE(O,re,B),ve=new $E(X,$,B,E),Te=new qy(X,lt,$),oe=new rM(X,lt,$),$.programs=Ie.programs,O.capabilities=B,O.extensions=lt,O.properties=se,O.renderLists=Fe,O.shadowMap=ot,O.state=E,O.info=$}b!==di&&(C=new hM(b,t.width,t.height,a,s,r));let Je=new pf(O,X);this.xr=Je,this.getContext=function(){return X},this.getContextAttributes=function(){return X.getContextAttributes()},this.forceContextLoss=function(){let R=lt.get("WEBGL_lose_context");R&&R.loseContext()},this.forceContextRestore=function(){let R=lt.get("WEBGL_lose_context");R&&R.restoreContext()},this.getPixelRatio=function(){return me},this.setPixelRatio=function(R){R!==void 0&&(me=R,this.setSize(ct,ae,!1))},this.getSize=function(R){return R.set(ct,ae)},this.setSize=function(R,G,ie=!0){if(Je.isPresenting){nt("WebGLRenderer: Can't change size while VR device is presenting.");return}ct=R,ae=G,t.width=Math.floor(R*me),t.height=Math.floor(G*me),ie===!0&&(t.style.width=R+"px",t.style.height=G+"px"),C!==null&&C.setSize(t.width,t.height),this.setViewport(0,0,R,G)},this.getDrawingBufferSize=function(R){return R.set(ct*me,ae*me).floor()},this.setDrawingBufferSize=function(R,G,ie){ct=R,ae=G,me=ie,t.width=Math.floor(R*ie),t.height=Math.floor(G*ie),this.setViewport(0,0,R,G)},this.setEffects=function(R){if(b===di){ht("WebGLRenderer: setEffects() requires outputBufferType set to HalfFloatType or FloatType.");return}if(R){for(let G=0;G<R.length;G++)if(R[G].isOutputPass===!0){nt("WebGLRenderer: OutputPass is not needed in setEffects(). Tone mapping and color space conversion are applied automatically.");break}}C.setEffects(R||[])},this.getCurrentViewport=function(R){return R.copy(le)},this.getViewport=function(R){return R.copy(Ge)},this.setViewport=function(R,G,ie,j){R.isVector4?Ge.set(R.x,R.y,R.z,R.w):Ge.set(R,G,ie,j),E.viewport(le.copy(Ge).multiplyScalar(me).round())},this.getScissor=function(R){return R.copy(Et)},this.setScissor=function(R,G,ie,j){R.isVector4?Et.set(R.x,R.y,R.z,R.w):Et.set(R,G,ie,j),E.scissor(Ee.copy(Et).multiplyScalar(me).round())},this.getScissorTest=function(){return pn},this.setScissorTest=function(R){E.setScissorTest(pn=R)},this.setOpaqueSort=function(R){qe=R},this.setTransparentSort=function(R){ft=R},this.getClearColor=function(R){return R.copy(xt.getClearColor())},this.setClearColor=function(){xt.setClearColor(...arguments)},this.getClearAlpha=function(){return xt.getClearAlpha()},this.setClearAlpha=function(){xt.setClearAlpha(...arguments)},this.clear=function(R=!0,G=!0,ie=!0){let j=0;if(R){let Z=!1;if(ye!==null){let Le=ye.texture.format;Z=g.has(Le)}if(Z){let Le=ye.texture.type,Ye=m.has(Le),Ne=xt.getClearColor(),Ke=xt.getClearAlpha(),$e=Ne.r,We=Ne.g,yt=Ne.b;Ye?(A[0]=$e,A[1]=We,A[2]=yt,A[3]=Ke,X.clearBufferuiv(X.COLOR,0,A)):(U[0]=$e,U[1]=We,U[2]=yt,U[3]=Ke,X.clearBufferiv(X.COLOR,0,U))}else j|=X.COLOR_BUFFER_BIT}G&&(j|=X.DEPTH_BUFFER_BIT,this.state.buffers.depth.setMask(!0)),ie&&(j|=X.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),j!==0&&X.clear(j)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.setNodesHandler=function(R){R.setRenderer(this),k=R},this.dispose=function(){t.removeEventListener("webglcontextlost",Xt,!1),t.removeEventListener("webglcontextrestored",De,!1),t.removeEventListener("webglcontextcreationerror",On,!1),xt.dispose(),Fe.dispose(),Se.dispose(),se.dispose(),we.dispose(),re.dispose(),He.dispose(),ve.dispose(),Ie.dispose(),Je.dispose(),Je.removeEventListener("sessionstart",mo),Je.removeEventListener("sessionend",go),zi.stop()};function Xt(R){R.preventDefault(),ja("WebGLRenderer: Context Lost."),H=!0}function De(){ja("WebGLRenderer: Context Restored."),H=!1;let R=$.autoReset,G=ot.enabled,ie=ot.autoUpdate,j=ot.needsUpdate,Z=ot.type;st(),$.autoReset=R,ot.enabled=G,ot.autoUpdate=ie,ot.needsUpdate=j,ot.type=Z}function On(R){ht("WebGLRenderer: A WebGL context could not be created. Reason: ",R.statusMessage)}function Jn(R){let G=R.target;G.removeEventListener("dispose",Jn),uo(G)}function uo(R){fo(R),se.remove(R)}function fo(R){let G=se.get(R).programs;G!==void 0&&(G.forEach(function(ie){Ie.releaseProgram(ie)}),R.isShaderMaterial&&Ie.releaseShaderCache(R))}this.renderBufferDirect=function(R,G,ie,j,Z,Le){G===null&&(G=xe);let Ye=Z.isMesh&&Z.matrixWorld.determinantAffine()<0,Ne=cs(R,G,ie,j,Z);E.setMaterial(j,Ye);let Ke=ie.index,$e=1;if(j.wireframe===!0){if(Ke=ce.getWireframeAttribute(ie),Ke===void 0)return;$e=2}let We=ie.drawRange,yt=ie.attributes.position,je=We.start*$e,kt=(We.start+We.count)*$e;Le!==null&&(je=Math.max(je,Le.start*$e),kt=Math.min(kt,(Le.start+Le.count)*$e)),Ke!==null?(je=Math.max(je,0),kt=Math.min(kt,Ke.count)):yt!=null&&(je=Math.max(je,0),kt=Math.min(kt,yt.count));let Pt=kt-je;if(Pt<0||Pt===1/0)return;He.setup(Z,j,Ne,ie,Ke);let Qt,Vt=Te;if(Ke!==null&&(Qt=Ae.get(Ke),Vt=oe,Vt.setIndex(Qt)),Z.isMesh)j.wireframe===!0?(E.setLineWidth(j.wireframeLinewidth*Rt()),Vt.setMode(X.LINES)):Vt.setMode(X.TRIANGLES);else if(Z.isLine){let Mt=j.linewidth;Mt===void 0&&(Mt=1),E.setLineWidth(Mt*Rt()),Z.isLineSegments?Vt.setMode(X.LINES):Z.isLineLoop?Vt.setMode(X.LINE_LOOP):Vt.setMode(X.LINE_STRIP)}else Z.isPoints?Vt.setMode(X.POINTS):Z.isSprite&&Vt.setMode(X.TRIANGLES);if(Z.isBatchedMesh)if(lt.get("WEBGL_multi_draw"))Vt.renderMultiDraw(Z._multiDrawStarts,Z._multiDrawCounts,Z._multiDrawCount);else{let Mt=Z._multiDrawStarts,Xe=Z._multiDrawCounts,Sn=Z._multiDrawCount,Ot=Ke?Ae.get(Ke).bytesPerElement:1,Qn=se.get(j).currentProgram.getUniforms();for(let mi=0;mi<Sn;mi++)Qn.setValue(X,"_gl_DrawID",mi),Vt.render(Mt[mi]/Ot,Xe[mi])}else if(Z.isInstancedMesh)Vt.renderInstances(je,Pt,Z.count);else if(ie.isInstancedBufferGeometry){let Mt=ie._maxInstanceCount!==void 0?ie._maxInstanceCount:1/0,Xe=Math.min(ie.instanceCount,Mt);Vt.renderInstances(je,Pt,Xe)}else Vt.render(je,Pt)};function Vi(R,G,ie,j){k!==null&&R.isNodeMaterial&&k.setObject(j,R),Ft===!0&&it.setState(R,ie,!1),R.transparent===!0&&R.side===mn&&R.forceSinglePass===!1?(R.side=Hn,R.needsUpdate=!0,Tn(R,G,j),R.side=Es,R.needsUpdate=!0,Tn(R,G,j),R.side=mn):Tn(R,G,j)}this.compile=function(R,G,ie=null){ie===null&&(ie=R),k!==null&&k.renderStart(R,G,ie),L=Se.get(ie),L.init(G),M.push(L),ie.traverseVisible(function(Z){Z.isLight&&Z.layers.test(G.layers)&&(L.pushLight(Z),Z.castShadow&&L.pushShadow(Z))}),R!==ie&&R.traverseVisible(function(Z){Z.isLight&&Z.layers.test(G.layers)&&(L.pushLight(Z),Z.castShadow&&L.pushShadow(Z))}),L.setupLights(),k!==null&&k.updateLights(L.state.lightsArray),Wt=this.localClippingEnabled,Ft=it.init(this.clippingPlanes,Wt),Ft===!0&&it.setGlobalState(this.clippingPlanes,G),k!==null&&ot.render(L.state.shadowsArray,ie,G);let j=new Set;return R.traverse(function(Z){if(!(Z.isMesh||Z.isPoints||Z.isLine||Z.isSprite))return;let Le=Z.material;if(Le)if(Array.isArray(Le))for(let Ye=0;Ye<Le.length;Ye++){let Ne=Le[Ye];Vi(Ne,ie,G,Z),j.add(Ne)}else Vi(Le,ie,G,Z),j.add(Le)}),L=M.pop(),k!==null&&k.renderEnd(),j},this.compileAsync=function(R,G,ie=null){let j=this.compile(R,G,ie);return new Promise(Z=>{function Le(){if(j.forEach(function(Ye){let Ke=se.get(Ye).currentProgram;(Ke===void 0||Ke.isReady())&&j.delete(Ye)}),j.size===0){Z(R);return}setTimeout(Le,10)}lt.get("KHR_parallel_shader_compile")!==null?Le():setTimeout(Le,10)})};let wr=null;function po(R){wr&&wr(R)}function mo(){zi.stop()}function go(){zi.start()}let zi=new I0;zi.setAnimationLoop(po),typeof self<"u"&&zi.setContext(self),this.setAnimationLoop=function(R){wr=R,Je.setAnimationLoop(R),R===null?zi.stop():zi.start()},Je.addEventListener("sessionstart",mo),Je.addEventListener("sessionend",go),this.render=function(R,G){if(G!==void 0&&G.isCamera!==!0){ht("WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(H===!0)return;k!==null&&k.renderStart(R,G);let ie=Je.enabled===!0&&Je.isPresenting===!0,j=C!==null&&(ye===null||ie)&&C.begin(O,ye);if(R.matrixWorldAutoUpdate===!0&&R.updateMatrixWorld(),G.parent===null&&G.matrixWorldAutoUpdate===!0&&G.updateMatrixWorld(),Je.enabled===!0&&Je.isPresenting===!0&&(C===null||C.isCompositing()===!1)&&(Je.cameraAutoUpdate===!0&&Je.updateCamera(G),G=Je.getCamera()),R.isScene===!0&&R.onBeforeRender(O,R,G,ye),L=Se.get(R,M.length),L.init(G),L.state.textureUnits=de.getTextureUnits(),M.push(L),Tt.multiplyMatrices(G.projectionMatrix,G.matrixWorldInverse),bt.setFromProjectionMatrix(Tt,ji,G.reversedDepth),Wt=this.localClippingEnabled,Ft=it.init(this.clippingPlanes,Wt),I=Fe.get(R,P.length),I.init(),P.push(I),Je.enabled===!0&&Je.isPresenting===!0){let Ye=O.xr.getDepthSensingMesh();Ye!==null&&Ai(Ye,G,-1/0,O.sortObjects)}Ai(R,G,0,O.sortObjects),I.finish(),k!==null&&k.updateLights(L.state.lightsArray),O.sortObjects===!0&&I.sort(qe,ft),vt=Je.enabled===!1||Je.isPresenting===!1||Je.hasDepthSensing()===!1,vt&&xt.addToRenderList(I,R),this.info.render.frame++,this.info.autoReset===!0&&this.info.reset(),Ft===!0&&it.beginShadows();let Z=L.state.shadowsArray;if(ot.render(Z,R,G),Ft===!0&&it.endShadows(),(j&&C.hasRenderPass())===!1){let Ye=I.opaque,Ne=I.transmissive;if(L.setupLights(),G.isArrayCamera){let Ke=G.cameras;if(Ne.length>0)for(let $e=0,We=Ke.length;$e<We;$e++){let yt=Ke[$e];Sa(Ye,Ne,R,yt)}vt&&xt.render(R);for(let $e=0,We=Ke.length;$e<We;$e++){let yt=Ke[$e];_o(I,R,yt,yt.viewport)}}else Ne.length>0&&Sa(Ye,Ne,R,G),vt&&xt.render(R),_o(I,R,G)}ye!==null&&ue===0&&(de.updateMultisampleRenderTarget(ye),de.updateRenderTargetMipmap(ye)),j&&C.end(O),R.isScene===!0&&R.onAfterRender(O,R,G),He.resetDefaultState(),V=-1,Q=null,M.pop(),M.length>0?(L=M[M.length-1],de.setTextureUnits(L.state.textureUnits),Ft===!0&&it.setGlobalState(O.clippingPlanes,L.state.camera)):L=null,P.pop(),P.length>0?I=P[P.length-1]:I=null,k!==null&&k.renderEnd()};function Ai(R,G,ie,j){if(R.visible===!1)return;if(R.layers.test(G.layers)){if(R.isGroup)ie=R.renderOrder;else if(R.isLOD)R.autoUpdate===!0&&R.update(G);else if(R.isLightProbeGrid)L.pushLightProbeGrid(R);else if(R.isLight)L.pushLight(R),R.castShadow&&L.pushShadow(R);else if(R.isSprite){if(!R.frustumCulled||R.intersectsFrustum(bt)){j&&bn.setFromMatrixPosition(R.matrixWorld).applyMatrix4(Tt);let Ye=re.update(R),Ne=R.material;Ne.visible&&I.push(R,Ye,Ne,ie,bn.z,null,G)}}else if((R.isMesh||R.isLine||R.isPoints)&&(!R.frustumCulled||R.intersectsFrustum(bt))){let Ye=re.update(R),Ne=R.material;if(j&&(R.boundingSphere!==void 0?(R.boundingSphere===null&&R.computeBoundingSphere(),bn.copy(R.boundingSphere.center)):(Ye.boundingSphere===null&&Ye.computeBoundingSphere(),bn.copy(Ye.boundingSphere.center)),bn.applyMatrix4(R.matrixWorld).applyMatrix4(Tt)),Array.isArray(Ne)){let Ke=Ye.groups;for(let $e=0,We=Ke.length;$e<We;$e++){let yt=Ke[$e],je=Ne[yt.materialIndex];je&&je.visible&&I.push(R,Ye,je,ie,bn.z,yt,G)}}else Ne.visible&&I.push(R,Ye,Ne,ie,bn.z,null,G)}}let Le=R.children;for(let Ye=0,Ne=Le.length;Ye<Ne;Ye++)Ai(Le[Ye],G,ie,j)}function _o(R,G,ie,j){let{opaque:Z,transmissive:Le,transparent:Ye}=R;L.setupLightsView(ie),Ft===!0&&it.setGlobalState(O.clippingPlanes,ie),j&&E.viewport(le.copy(j)),Z.length>0&&si(Z,G,ie),Le.length>0&&si(Le,G,ie),Ye.length>0&&si(Ye,G,ie),E.buffers.depth.setTest(!0),E.buffers.depth.setMask(!0),E.buffers.color.setMask(!0),E.setPolygonOffset(!1)}function Sa(R,G,ie,j){if((ie.isScene===!0?ie.overrideMaterial:null)!==null)return;if(L.state.transmissionRenderTarget[j.id]===void 0){let je=lt.has("EXT_color_buffer_half_float")||lt.has("EXT_color_buffer_float");L.state.transmissionRenderTarget[j.id]=new ai(1,1,{generateMipmaps:!0,type:je?rs:di,minFilter:is,samples:Math.max(4,B.samples),stencilBuffer:r,resolveDepthBuffer:!1,resolveStencilBuffer:!1,storeMultisampledDepthBuffer:!1,storeMultisampledStencilBuffer:!1,colorSpace:It.workingColorSpace})}let Le=L.state.transmissionRenderTarget[j.id],Ye=j.viewport||le;Le.setSize(Ye.z*O.transmissionResolutionScale,Ye.w*O.transmissionResolutionScale);let Ne=O.getRenderTarget(),Ke=O.getActiveCubeFace(),$e=O.getActiveMipmapLevel();O.setRenderTarget(Le),O.getClearColor(ut),et=O.getClearAlpha(),et<1&&O.setClearColor(16777215,.5),O.clear(),vt&&xt.render(ie);let We=O.toneMapping;O.toneMapping=ns;let yt=j.viewport;if(j.viewport!==void 0&&(j.viewport=void 0),L.setupLightsView(j),Ft===!0&&it.setGlobalState(O.clippingPlanes,j),si(R,ie,j),de.updateMultisampleRenderTarget(Le),de.updateRenderTargetMipmap(Le),lt.has("WEBGL_multisampled_render_to_texture")===!1){let je=!1;for(let kt=0,Pt=G.length;kt<Pt;kt++){let Qt=G[kt],{object:Vt,geometry:Mt,material:Xe,group:Sn}=Qt;if(Xe.side===mn&&Vt.layers.test(j.layers)){let Ot=Xe.side;Xe.side=Hn,Xe.needsUpdate=!0,Gi(Vt,ie,j,Mt,Xe,Sn),Xe.side=Ot,Xe.needsUpdate=!0,je=!0}}je===!0&&(de.updateMultisampleRenderTarget(Le),de.updateRenderTargetMipmap(Le))}O.setRenderTarget(Ne,Ke,$e),O.setClearColor(ut,et),yt!==void 0&&(j.viewport=yt),O.toneMapping=We}function si(R,G,ie){let j=G.isScene===!0?G.overrideMaterial:null;for(let Z=0,Le=R.length;Z<Le;Z++){let Ye=R[Z],{object:Ne,geometry:Ke,group:$e}=Ye,We=Ye.material;We.allowOverride===!0&&j!==null&&(We=j),Ne.layers.test(ie.layers)&&Gi(Ne,G,ie,Ke,We,$e)}}function Gi(R,G,ie,j,Z,Le){k!==null&&Z.isNodeMaterial&&k.setObject(R,Z),R.onBeforeRender(O,G,ie,j,Z,Le),R.modelViewMatrix.multiplyMatrices(ie.matrixWorldInverse,R.matrixWorld),R.normalMatrix.getNormalMatrix(R.modelViewMatrix),Z.onBeforeRender(O,G,ie,j,R,Le),Z.transparent===!0&&Z.side===mn&&Z.forceSinglePass===!1?(Z.side=Hn,Z.needsUpdate=!0,O.renderBufferDirect(ie,G,j,Z,R,Le),Z.side=Es,Z.needsUpdate=!0,O.renderBufferDirect(ie,G,j,Z,R,Le),Z.side=mn):O.renderBufferDirect(ie,G,j,Z,R,Le),R.onAfterRender(O,G,ie,j,Z,Le)}function Tn(R,G,ie){G.isScene!==!0&&(G=xe);let j=se.get(R),Z=L.state.lights,Le=L.state.shadowsArray,Ye=Z.state.version,Ne=Ie.getParameters(R,Z.state,Le,G,ie,L.state.lightProbeGridArray),Ke=Ie.getProgramCacheKey(Ne),$e=j.programs;j.environment=R.isMeshStandardMaterial||R.isMeshLambertMaterial||R.isMeshPhongMaterial?G.environment:null,j.fog=G.fog;let We=R.isMeshStandardMaterial||R.isMeshLambertMaterial&&!R.envMap||R.isMeshPhongMaterial&&!R.envMap;j.envMap=we.get(R.envMap||j.environment,We),j.envMapRotation=j.environment!==null&&R.envMap===null?G.environmentRotation:R.envMapRotation,$e===void 0&&(R.addEventListener("dispose",Jn),$e=new Map,j.programs=$e);let yt=$e.get(Ke);if(yt!==void 0){if(j.currentProgram===yt&&j.lightsStateVersion===Ye)return Ar(R,Ne),yt}else Ne.uniforms=Ie.getUniforms(R),k!==null&&R.isNodeMaterial&&k.build(R,ie,Ne),R.onBeforeCompile(Ne,O),yt=Ie.acquireProgram(Ne,Ke),$e.set(Ke,yt),j.uniforms=Ne.uniforms;let je=j.uniforms;return(!R.isShaderMaterial&&!R.isRawShaderMaterial||R.clipping===!0)&&(je.clippingPlanes=it.uniform),Ar(R,Ne),j.needsLights=tr(R),j.lightsStateVersion=Ye,j.needsLights&&(je.ambientLightColor.value=Z.state.ambient,je.lightProbe.value=Z.state.probe,je.sunLights.value=Z.state.sun,je.sunLightShadows.value=Z.state.sunShadow,je.directionalLights.value=Z.state.directional,je.directionalLightShadows.value=Z.state.directionalShadow,je.spotLights.value=Z.state.spot,je.spotLightShadows.value=Z.state.spotShadow,je.rectAreaLights.value=Z.state.rectArea,je.ltc_1.value=Z.state.rectAreaLTC1,je.ltc_2.value=Z.state.rectAreaLTC2,je.pointLights.value=Z.state.point,je.pointLightShadows.value=Z.state.pointShadow,je.hemisphereLights.value=Z.state.hemi,je.sunShadowMatrix.value=Z.state.sunShadowMatrix,je.sunShadowCascade.value=Z.state.sunShadowCascade,je.directionalShadowMatrix.value=Z.state.directionalShadowMatrix,je.spotLightMatrix.value=Z.state.spotLightMatrix,je.spotLightMap.value=Z.state.spotLightMap,je.pointShadowMatrix.value=Z.state.pointShadowMatrix),j.lightProbeGrid=L.state.lightProbeGridArray.length>0,j.currentProgram=yt,j.uniformsList=null,yt}function qt(R){if(R.uniformsList===null){let G=R.currentProgram.getUniforms();R.uniformsList=fa.seqWithValue(G.seq,R.uniforms)}return R.uniformsList}function Ar(R,G){let ie=se.get(R);ie.outputColorSpace=G.outputColorSpace,ie.batching=G.batching,ie.batchingColor=G.batchingColor,ie.instancing=G.instancing,ie.instancingColor=G.instancingColor,ie.instancingMorph=G.instancingMorph,ie.skinning=G.skinning,ie.morphTargets=G.morphTargets,ie.morphNormals=G.morphNormals,ie.morphColors=G.morphColors,ie.morphTargetsCount=G.morphTargetsCount,ie.numClippingPlanes=G.numClippingPlanes,ie.numIntersection=G.numClipIntersection,ie.vertexAlphas=G.vertexAlphas,ie.vertexTangents=G.vertexTangents,ie.toneMapping=G.toneMapping}function Xl(R,G){if(R.length===0)return null;if(R.length===1)return R[0].texture!==null?R[0]:null;T.setFromMatrixPosition(G.matrixWorld);for(let ie=0,j=R.length;ie<j;ie++){let Z=R[ie];if(Z.texture!==null&&Z.boundingBox.containsPoint(T))return Z}return null}function cs(R,G,ie,j,Z){G.isScene!==!0&&(G=xe),de.resetTextureUnits();let Le=G.fog,Ye=j.isMeshStandardMaterial||j.isMeshLambertMaterial||j.isMeshPhongMaterial?G.environment:null,Ne=ye===null?O.outputColorSpace:ye.isXRRenderTarget===!0?ye.texture.colorSpace:It.workingColorSpace,Ke=j.isMeshStandardMaterial||j.isMeshLambertMaterial&&!j.envMap||j.isMeshPhongMaterial&&!j.envMap,$e=we.get(j.envMap||Ye,Ke),We=j.vertexColors===!0&&!!ie.attributes.color&&ie.attributes.color.itemSize===4,yt=!!ie.attributes.tangent&&(!!j.normalMap||j.anisotropy>0),je=!!ie.morphAttributes.position,kt=!!ie.morphAttributes.normal,Pt=!!ie.morphAttributes.color,Qt=ns;j.toneMapped&&(ye===null||ye.isXRRenderTarget===!0)&&(Qt=O.toneMapping);let Vt=ie.morphAttributes.position||ie.morphAttributes.normal||ie.morphAttributes.color,Mt=Vt!==void 0?Vt.length:0,Xe=se.get(j),Sn=L.state.lights;if(Ft===!0&&(Wt===!0||R!==Q)){let Bt=R===Q&&j.id===V;it.setState(j,R,Bt)}let Ot=!1;j.version===Xe.__version?(Xe.needsLights&&Xe.lightsStateVersion!==Sn.state.version||Xe.outputColorSpace!==Ne||Z.isBatchedMesh&&Xe.batching===!1||!Z.isBatchedMesh&&Xe.batching===!0||Z.isBatchedMesh&&Xe.batchingColor===!0&&Z._colorsTexture===null||Z.isBatchedMesh&&Xe.batchingColor===!1&&Z._colorsTexture!==null||Z.isInstancedMesh&&Xe.instancing===!1||!Z.isInstancedMesh&&Xe.instancing===!0||Z.isSkinnedMesh&&Xe.skinning===!1||!Z.isSkinnedMesh&&Xe.skinning===!0||Z.isInstancedMesh&&Xe.instancingColor===!0&&Z.instanceColor===null||Z.isInstancedMesh&&Xe.instancingColor===!1&&Z.instanceColor!==null||Z.isInstancedMesh&&Xe.instancingMorph===!0&&Z.morphTexture===null||Z.isInstancedMesh&&Xe.instancingMorph===!1&&Z.morphTexture!==null||Xe.envMap!==$e||j.fog===!0&&Xe.fog!==Le||Xe.numClippingPlanes!==void 0&&(Xe.numClippingPlanes!==it.numPlanes||Xe.numIntersection!==it.numIntersection)||Xe.vertexAlphas!==We||Xe.vertexTangents!==yt||Xe.morphTargets!==je||Xe.morphNormals!==kt||Xe.morphColors!==Pt||Xe.toneMapping!==Qt||Xe.morphTargetsCount!==Mt||!!Xe.lightProbeGrid!=L.state.lightProbeGridArray.length>0)&&(Ot=!0):(Ot=!0,Xe.__version=j.version);let Qn=Xe.currentProgram;Ot===!0&&(Qn=Tn(j,G,Z),k&&j.isNodeMaterial&&k.onUpdateProgram(j,Qn,Xe));let mi=!1,us=!1,hn=!1,Nt=Qn.getUniforms(),Ct=Xe.uniforms;if(E.useProgram(Qn.program)&&(mi=!0,us=!0,hn=!0),j.id!==V&&(V=j.id,us=!0),Xe.needsLights){let Bt=Xl(L.state.lightProbeGridArray,Z);Xe.lightProbeGrid!==Bt&&(Xe.lightProbeGrid=Bt,us=!0)}if(mi||Q!==R){E.buffers.depth.getReversed()&&R.reversedDepth!==!0&&(R._reversedDepth=!0,R.updateProjectionMatrix()),Nt.setValue(X,"projectionMatrix",R.projectionMatrix),Nt.setValue(X,"viewMatrix",R.matrixWorldInverse);let ri=Nt.map.cameraPosition;ri!==void 0&&ri.setValue(X,Jt.setFromMatrixPosition(R.matrixWorld)),B.logarithmicDepthBuffer&&Nt.setValue(X,"logDepthBufFC",2/(Math.log(R.far+1)/Math.LN2)),(j.isMeshPhongMaterial||j.isMeshToonMaterial||j.isMeshLambertMaterial||j.isMeshBasicMaterial||j.isMeshStandardMaterial||j.isShaderMaterial)&&Nt.setValue(X,"isOrthographic",R.isOrthographicCamera===!0),Q!==R&&(Q=R,us=!0,hn=!0)}if(Xe.needsLights&&(Sn.state.sunShadowMap.length>0&&Nt.setValue(X,"sunShadowMap",Sn.state.sunShadowMap,de),Sn.state.directionalShadowMap.length>0&&Nt.setValue(X,"directionalShadowMap",Sn.state.directionalShadowMap,de),Sn.state.spotShadowMap.length>0&&Nt.setValue(X,"spotShadowMap",Sn.state.spotShadowMap,de),Sn.state.pointShadowMap.length>0&&Nt.setValue(X,"pointShadowMap",Sn.state.pointShadowMap,de)),Z.isSkinnedMesh){Nt.setOptional(X,Z,"bindMatrix"),Nt.setOptional(X,Z,"bindMatrixInverse");let Bt=Z.skeleton;Bt&&(Bt.boneTexture===null&&Bt.computeBoneTexture(),Nt.setValue(X,"boneTexture",Bt.boneTexture,de))}Z.isBatchedMesh&&(Nt.setOptional(X,Z,"batchingTexture"),Nt.setValue(X,"batchingTexture",Z._matricesTexture,de),Nt.setOptional(X,Z,"batchingIdTexture"),Nt.setValue(X,"batchingIdTexture",Z._indirectTexture,de),Nt.setOptional(X,Z,"batchingColorTexture"),Z._colorsTexture!==null&&Nt.setValue(X,"batchingColorTexture",Z._colorsTexture,de));let Wn=ie.morphAttributes;if((Wn.position!==void 0||Wn.normal!==void 0||Wn.color!==void 0)&&W.update(Z,ie,Qn),(us||Xe.receiveShadow!==Z.receiveShadow)&&(Xe.receiveShadow=Z.receiveShadow,Nt.setValue(X,"receiveShadow",Z.receiveShadow)),(j.isMeshStandardMaterial||j.isMeshLambertMaterial||j.isMeshPhongMaterial)&&j.envMap===null&&G.environment!==null&&(Ct.envMapIntensity.value=G.environmentIntensity),Ct.dfgLUT!==void 0&&(Ct.dfgLUT.value=KE()),us){if(Nt.setValue(X,"toneMappingExposure",O.toneMappingExposure),Xe.needsLights&&hs(Ct,hn),Le&&j.fog===!0&&Ze.refreshFogUniforms(Ct,Le),Ze.refreshMaterialUniforms(Ct,j,me,ae,L.state.transmissionRenderTarget[R.id]),Xe.needsLights&&Xe.lightProbeGrid){let Bt=Xe.lightProbeGrid;Ct.probesSH.value=Bt.texture,Ct.probesMin.value.copy(Bt.boundingBox.min),Ct.probesMax.value.copy(Bt.boundingBox.max),Ct.probesResolution.value.copy(Bt.resolution)}fa.upload(X,qt(Xe),Ct,de)}if(j.isShaderMaterial&&j.uniformsNeedUpdate===!0&&(fa.upload(X,qt(Xe),Ct,de),j.uniformsNeedUpdate=!1),j.isSpriteMaterial&&Nt.setValue(X,"center",Z.center),Nt.setValue(X,"modelViewMatrix",Z.modelViewMatrix),Nt.setValue(X,"normalMatrix",Z.normalMatrix),Nt.setValue(X,"modelMatrix",Z.matrixWorld),j.uniformsGroups!==void 0){let Bt=j.uniformsGroups;for(let ri=0,ds=Bt.length;ri<ds;ri++){let Ls=Bt[ri];ve.update(Ls,Qn),ve.bind(Ls,Qn)}}return Qn}function hs(R,G){R.ambientLightColor.needsUpdate=G,R.lightProbe.needsUpdate=G,R.sunLights.needsUpdate=G,R.sunLightShadows.needsUpdate=G,R.directionalLights.needsUpdate=G,R.directionalLightShadows.needsUpdate=G,R.pointLights.needsUpdate=G,R.pointLightShadows.needsUpdate=G,R.spotLights.needsUpdate=G,R.spotLightShadows.needsUpdate=G,R.rectAreaLights.needsUpdate=G,R.hemisphereLights.needsUpdate=G}function tr(R){return R.isMeshLambertMaterial||R.isMeshToonMaterial||R.isMeshPhongMaterial||R.isMeshStandardMaterial||R.isShadowMaterial||R.isShaderMaterial&&R.lights===!0}this.getActiveCubeFace=function(){return he},this.getActiveMipmapLevel=function(){return ue},this.getRenderTarget=function(){return ye},this.setRenderTargetTextures=function(R,G,ie){let j=se.get(R);j.__autoAllocateDepthBuffer=R.resolveDepthBuffer===!1,j.__autoAllocateDepthBuffer===!1&&(j.__useRenderToTexture=!1),se.get(R.texture).__webglTexture=G,se.get(R.depthTexture).__webglTexture=j.__autoAllocateDepthBuffer?void 0:ie,j.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(R,G){let ie=se.get(R);ie.__webglFramebuffer=G,ie.__useDefaultFramebuffer=G===void 0},this.setRenderTarget=function(R,G=0,ie=0){ye=R,he=G,ue=ie;let j=null,Z=!1,Le=!1;if(R){let Ne=se.get(R);if(Ne.__useDefaultFramebuffer!==void 0){E.bindFramebuffer(X.FRAMEBUFFER,Ne.__webglFramebuffer),le.copy(R.viewport),Ee.copy(R.scissor),be=R.scissorTest,E.viewport(le),E.scissor(Ee),E.setScissorTest(be),V=-1;return}else if(Ne.__webglFramebuffer===void 0)de.setupRenderTarget(R);else if(Ne.__hasExternalTextures)de.rebindTextures(R,se.get(R.texture).__webglTexture,se.get(R.depthTexture).__webglTexture);else if(R.depthBuffer){let We=R.depthTexture;if(Ne.__boundDepthTexture!==We){if(We!==null&&se.has(We)&&(R.width!==We.image.width||R.height!==We.image.height))throw new Error("THREE.WebGLRenderer: Attached DepthTexture is initialized to the incorrect size.");de.setupDepthRenderbuffer(R)}}let Ke=R.texture;(Ke.isData3DTexture||Ke.isDataArrayTexture||Ke.isCompressedArrayTexture)&&(Le=!0);let $e=se.get(R).__webglFramebuffer;R.isWebGLCubeRenderTarget?(Array.isArray($e[G])?j=$e[G][ie]:j=$e[G],Z=!0):R.samples>0&&de.useMultisampledRTT(R)===!1?j=se.get(R).__webglMultisampledFramebuffer:Array.isArray($e)?j=$e[ie]:j=$e,le.copy(R.viewport),Ee.copy(R.scissor),be=R.scissorTest}else le.copy(Ge).multiplyScalar(me).floor(),Ee.copy(Et).multiplyScalar(me).floor(),be=pn;if(ie!==0&&(j=q),E.bindFramebuffer(X.FRAMEBUFFER,j)&&E.drawBuffers(R,j),E.viewport(le),E.scissor(Ee),E.setScissorTest(be),Z){let Ne=se.get(R.texture);X.framebufferTexture2D(X.FRAMEBUFFER,X.COLOR_ATTACHMENT0,X.TEXTURE_CUBE_MAP_POSITIVE_X+G,Ne.__webglTexture,ie)}else if(Le){let Ne=G;for(let Ke=0;Ke<R.textures.length;Ke++){let $e=se.get(R.textures[Ke]);X.framebufferTextureLayer(X.FRAMEBUFFER,X.COLOR_ATTACHMENT0+Ke,$e.__webglTexture,ie,Ne)}}else if(R!==null&&ie!==0){let Ne=se.get(R.texture);X.framebufferTexture2D(X.FRAMEBUFFER,X.COLOR_ATTACHMENT0,X.TEXTURE_2D,Ne.__webglTexture,ie)}V=-1};function Ps(R){let G=se.get(R);return(G.__readFormat!==R.format||G.__readType!==R.type)&&(G.__readFormat=R.format,G.__readType=R.type,G.__formatReadable=B.textureFormatReadable(R.format),G.__typeReadable=B.textureTypeReadable(R.type)),G}this.readRenderTargetPixels=function(R,G,ie,j,Z,Le,Ye,Ne=0){if(!(R&&R.isWebGLRenderTarget)){ht("WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Ke=se.get(R).__webglFramebuffer;if(R.isWebGLCubeRenderTarget&&Ye!==void 0&&(Ke=Ke[Ye]),Ke){E.bindFramebuffer(X.FRAMEBUFFER,Ke);try{let $e=R.textures[Ne],We=$e.format,yt=$e.type;R.textures.length>1&&X.readBuffer(X.COLOR_ATTACHMENT0+Ne);let je=Ps($e);if(je.__formatReadable===!1){ht("WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(je.__typeReadable===!1){ht("WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}G>=0&&G<=R.width-j&&ie>=0&&ie<=R.height-Z&&X.readPixels(G,ie,j,Z,Re.convert(We),Re.convert(yt),Le)}finally{let $e=ye!==null?se.get(ye).__webglFramebuffer:null;E.bindFramebuffer(X.FRAMEBUFFER,$e)}}},this.readRenderTargetPixelsAsync=async function(R,G,ie,j,Z,Le,Ye,Ne=0){if(!(R&&R.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Ke=se.get(R).__webglFramebuffer;if(R.isWebGLCubeRenderTarget&&Ye!==void 0&&(Ke=Ke[Ye]),Ke)if(G>=0&&G<=R.width-j&&ie>=0&&ie<=R.height-Z){E.bindFramebuffer(X.FRAMEBUFFER,Ke);let $e=R.textures[Ne],We=$e.format,yt=$e.type;R.textures.length>1&&X.readBuffer(X.COLOR_ATTACHMENT0+Ne);let je=Ps($e);if(je.__formatReadable===!1)throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(je.__typeReadable===!1)throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");let kt=X.createBuffer();X.bindBuffer(X.PIXEL_PACK_BUFFER,kt),X.bufferData(X.PIXEL_PACK_BUFFER,Le.byteLength,X.STREAM_READ),X.readPixels(G,ie,j,Z,Re.convert(We),Re.convert(yt),0),X.bindBuffer(X.PIXEL_PACK_BUFFER,null);let Pt=ye!==null?se.get(ye).__webglFramebuffer:null;E.bindFramebuffer(X.FRAMEBUFFER,Pt);let Qt=X.fenceSync(X.SYNC_GPU_COMMANDS_COMPLETE,0);return X.flush(),await i0(X,Qt,4),X.bindBuffer(X.PIXEL_PACK_BUFFER,kt),X.getBufferSubData(X.PIXEL_PACK_BUFFER,0,Le),X.bindBuffer(X.PIXEL_PACK_BUFFER,null),X.deleteBuffer(kt),X.deleteSync(Qt),Le}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(R,G=null,ie=0){let j=Math.pow(2,-ie),Z=Math.floor(R.image.width*j),Le=Math.floor(R.image.height*j),Ye=G!==null?G.x:0,Ne=G!==null?G.y:0;de.setTexture2D(R,0),X.copyTexSubImage2D(X.TEXTURE_2D,ie,0,0,Ye,Ne,Z,Le),E.unbindTexture()},this.copyTextureToTexture=function(R,G,ie=null,j=null,Z=0,Le=0){let Ye,Ne,Ke,$e,We,yt,je,kt,Pt,Qt=R.isCompressedTexture?R.mipmaps[Le]:R.image;if(ie!==null)Ye=ie.max.x-ie.min.x,Ne=ie.max.y-ie.min.y,Ke=ie.isBox3?ie.max.z-ie.min.z:1,$e=ie.min.x,We=ie.min.y,yt=ie.isBox3?ie.min.z:0;else{let Ct=Math.pow(2,-Z);Ye=Math.floor(Qt.width*Ct),Ne=Math.floor(Qt.height*Ct),R.isDataArrayTexture?Ke=Qt.depth:R.isData3DTexture?Ke=Math.floor(Qt.depth*Ct):Ke=1,$e=0,We=0,yt=0}j!==null?(je=j.x,kt=j.y,Pt=j.z):(je=0,kt=0,Pt=0);let Vt=Re.convert(G.format),Mt=Re.convert(G.type),Xe;G.isData3DTexture?(de.setTexture3D(G,0),Xe=X.TEXTURE_3D):G.isDataArrayTexture||G.isCompressedArrayTexture?(de.setTexture2DArray(G,0),Xe=X.TEXTURE_2D_ARRAY):(de.setTexture2D(G,0),Xe=X.TEXTURE_2D),E.activeTexture(X.TEXTURE0),E.pixelStorei(X.UNPACK_FLIP_Y_WEBGL,G.flipY),E.pixelStorei(X.UNPACK_PREMULTIPLY_ALPHA_WEBGL,G.premultiplyAlpha),E.pixelStorei(X.UNPACK_ALIGNMENT,G.unpackAlignment);let Sn=E.getParameter(X.UNPACK_ROW_LENGTH),Ot=E.getParameter(X.UNPACK_IMAGE_HEIGHT),Qn=E.getParameter(X.UNPACK_SKIP_PIXELS),mi=E.getParameter(X.UNPACK_SKIP_ROWS),us=E.getParameter(X.UNPACK_SKIP_IMAGES);E.pixelStorei(X.UNPACK_ROW_LENGTH,Qt.width),E.pixelStorei(X.UNPACK_IMAGE_HEIGHT,Qt.height),E.pixelStorei(X.UNPACK_SKIP_PIXELS,$e),E.pixelStorei(X.UNPACK_SKIP_ROWS,We),E.pixelStorei(X.UNPACK_SKIP_IMAGES,yt);let hn=R.isDataArrayTexture||R.isData3DTexture,Nt=G.isDataArrayTexture||G.isData3DTexture;if(R.isDepthTexture){let Ct=se.get(R),Wn=se.get(G),Bt=se.get(Ct.__renderTarget),ri=se.get(Wn.__renderTarget);E.bindFramebuffer(X.READ_FRAMEBUFFER,Bt.__webglFramebuffer),E.bindFramebuffer(X.DRAW_FRAMEBUFFER,ri.__webglFramebuffer);for(let ds=0;ds<Ke;ds++)hn&&(X.framebufferTextureLayer(X.READ_FRAMEBUFFER,X.COLOR_ATTACHMENT0,se.get(R).__webglTexture,Z,yt+ds),X.framebufferTextureLayer(X.DRAW_FRAMEBUFFER,X.COLOR_ATTACHMENT0,se.get(G).__webglTexture,Le,Pt+ds)),X.blitFramebuffer($e,We,Ye,Ne,je,kt,Ye,Ne,X.DEPTH_BUFFER_BIT,X.NEAREST);E.bindFramebuffer(X.READ_FRAMEBUFFER,null),E.bindFramebuffer(X.DRAW_FRAMEBUFFER,null)}else if(Z!==0||R.isRenderTargetTexture||se.has(R)){let Ct=se.get(R),Wn=se.get(G);E.bindFramebuffer(X.READ_FRAMEBUFFER,z),E.bindFramebuffer(X.DRAW_FRAMEBUFFER,ee);for(let Bt=0;Bt<Ke;Bt++)hn?X.framebufferTextureLayer(X.READ_FRAMEBUFFER,X.COLOR_ATTACHMENT0,Ct.__webglTexture,Z,yt+Bt):X.framebufferTexture2D(X.READ_FRAMEBUFFER,X.COLOR_ATTACHMENT0,X.TEXTURE_2D,Ct.__webglTexture,Z),Nt?X.framebufferTextureLayer(X.DRAW_FRAMEBUFFER,X.COLOR_ATTACHMENT0,Wn.__webglTexture,Le,Pt+Bt):X.framebufferTexture2D(X.DRAW_FRAMEBUFFER,X.COLOR_ATTACHMENT0,X.TEXTURE_2D,Wn.__webglTexture,Le),Z!==0?X.blitFramebuffer($e,We,Ye,Ne,je,kt,Ye,Ne,X.COLOR_BUFFER_BIT,X.NEAREST):Nt?X.copyTexSubImage3D(Xe,Le,je,kt,Pt+Bt,$e,We,Ye,Ne):X.copyTexSubImage2D(Xe,Le,je,kt,$e,We,Ye,Ne);E.bindFramebuffer(X.READ_FRAMEBUFFER,null),E.bindFramebuffer(X.DRAW_FRAMEBUFFER,null)}else Nt?R.isDataTexture||R.isData3DTexture?X.texSubImage3D(Xe,Le,je,kt,Pt,Ye,Ne,Ke,Vt,Mt,Qt.data):G.isCompressedArrayTexture?X.compressedTexSubImage3D(Xe,Le,je,kt,Pt,Ye,Ne,Ke,Vt,Qt.data):X.texSubImage3D(Xe,Le,je,kt,Pt,Ye,Ne,Ke,Vt,Mt,Qt):R.isDataTexture?X.texSubImage2D(X.TEXTURE_2D,Le,je,kt,Ye,Ne,Vt,Mt,Qt.data):R.isCompressedTexture?X.compressedTexSubImage2D(X.TEXTURE_2D,Le,je,kt,Qt.width,Qt.height,Vt,Qt.data):X.texSubImage2D(X.TEXTURE_2D,Le,je,kt,Ye,Ne,Vt,Mt,Qt);E.pixelStorei(X.UNPACK_ROW_LENGTH,Sn),E.pixelStorei(X.UNPACK_IMAGE_HEIGHT,Ot),E.pixelStorei(X.UNPACK_SKIP_PIXELS,Qn),E.pixelStorei(X.UNPACK_SKIP_ROWS,mi),E.pixelStorei(X.UNPACK_SKIP_IMAGES,us),Le===0&&G.generateMipmaps&&X.generateMipmap(Xe),E.unbindTexture()},this.initRenderTarget=function(R){se.get(R).__webglFramebuffer===void 0&&de.setupRenderTarget(R)},this.initTexture=function(R){R.isCubeTexture?de.setTextureCube(R,0):R.isData3DTexture?de.setTexture3D(R,0):R.isDataArrayTexture||R.isCompressedArrayTexture?de.setTexture2DArray(R,0):de.setTexture2D(R,0),E.unbindTexture()},this.resetState=function(){he=0,ue=0,ye=null,E.reset(),He.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return ji}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;let t=this.getContext();t.drawingBufferColorSpace=It._getDrawingBufferColorSpace(e),t.unpackColorSpace=It._getUnpackColorSpace()}};var O0={type:"change"},_f={type:"start"},H0={type:"end"},fu=new vs,B0=new Bn,jE=Math.cos(70*Zs.DEG2RAD),Dn=new y,fi=2*Math.PI,Zt={NONE:-1,ROTATE:0,DOLLY:1,PAN:2,TOUCH_ROTATE:3,TOUCH_PAN:4,TOUCH_DOLLY_PAN:5,TOUCH_DOLLY_ROTATE:6},gf=1e-6,pu=class extends vl{constructor(e,t=null){super(e,t),this.state=Zt.NONE,this.target=new y,this.cursor=new y,this.minDistance=0,this.maxDistance=1/0,this.minZoom=0,this.maxZoom=1/0,this.minTargetRadius=0,this.maxTargetRadius=1/0,this.minPolarAngle=0,this.maxPolarAngle=Math.PI,this.minAzimuthAngle=-1/0,this.maxAzimuthAngle=1/0,this.enableDamping=!1,this.dampingFactor=.05,this.enableZoom=!0,this.zoomSpeed=1,this.enableRotate=!0,this.rotateSpeed=1,this.keyRotateSpeed=1,this.enablePan=!0,this.panSpeed=1,this.screenSpacePanning=!0,this.keyPanSpeed=7,this.zoomToCursor=!1,this.autoRotate=!1,this.autoRotateSpeed=2,this.keys={LEFT:"ArrowLeft",UP:"ArrowUp",RIGHT:"ArrowRight",BOTTOM:"ArrowDown"},this.mouseButtons={LEFT:Ni.ROTATE,MIDDLE:Ni.DOLLY,RIGHT:Ni.PAN},this.touches={ONE:ts.ROTATE,TWO:ts.DOLLY_PAN},this.target0=this.target.clone(),this.position0=this.object.position.clone(),this.zoom0=this.object.zoom,this._cursorStyle="auto",this._domElementKeyEvents=null,this._lastPosition=new y,this._lastQuaternion=new rn,this._lastTargetPosition=new y,this._quat=new rn().setFromUnitVectors(e.up,new y(0,1,0)),this._quatInverse=this._quat.clone().invert(),this._spherical=new sa,this._sphericalDelta=new sa,this._scale=1,this._panOffset=new y,this._rotateStart=new Pe,this._rotateEnd=new Pe,this._rotateDelta=new Pe,this._panStart=new Pe,this._panEnd=new Pe,this._panDelta=new Pe,this._dollyStart=new Pe,this._dollyEnd=new Pe,this._dollyDelta=new Pe,this._dollyDirection=new y,this._mouse=new Pe,this._performCursorZoom=!1,this._pointers=[],this._pointerPositions={},this._controlActive=!1,this._onPointerMove=QE.bind(this),this._onPointerDown=JE.bind(this),this._onPointerUp=e1.bind(this),this._onContextMenu=a1.bind(this),this._onMouseWheel=i1.bind(this),this._onKeyDown=s1.bind(this),this._onTouchStart=r1.bind(this),this._onTouchMove=o1.bind(this),this._onMouseDown=t1.bind(this),this._onMouseMove=n1.bind(this),this._interceptControlDown=l1.bind(this),this._interceptControlUp=c1.bind(this),this.domElement!==null&&this.connect(this.domElement),this.update()}set cursorStyle(e){this._cursorStyle=e,e==="grab"?this.domElement.style.cursor="grab":this.domElement.style.cursor="auto"}get cursorStyle(){return this._cursorStyle}connect(e){super.connect(e),this.domElement.addEventListener("pointerdown",this._onPointerDown),this.domElement.addEventListener("pointercancel",this._onPointerUp),this.domElement.addEventListener("contextmenu",this._onContextMenu),this.domElement.addEventListener("wheel",this._onMouseWheel,{passive:!1}),this.domElement.getRootNode().addEventListener("keydown",this._interceptControlDown,{passive:!0,capture:!0}),this.domElement.style.touchAction="none"}disconnect(){this.state=Zt.NONE,this.domElement.removeEventListener("pointerdown",this._onPointerDown),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.domElement.removeEventListener("pointercancel",this._onPointerUp),this.domElement.removeEventListener("wheel",this._onMouseWheel),this.domElement.removeEventListener("contextmenu",this._onContextMenu),this.stopListenToKeyEvents();let e=this.domElement.getRootNode();e.removeEventListener("keydown",this._interceptControlDown,{capture:!0}),e.removeEventListener("keyup",this._interceptControlUp,{capture:!0}),this._controlActive=!1,this._pointers.length=0,this._pointerPositions={},this.domElement.style.touchAction="",this.domElement.style.cursor="auto"}dispose(){this.disconnect()}getPolarAngle(){return this._spherical.phi}getAzimuthalAngle(){return this._spherical.theta}getDistance(){return this.object.position.distanceTo(this.target)}listenToKeyEvents(e){e.addEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=e}stopListenToKeyEvents(){this._domElementKeyEvents!==null&&(this._domElementKeyEvents.removeEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=null)}saveState(){this.target0.copy(this.target),this.position0.copy(this.object.position),this.zoom0=this.object.zoom}reset(){this.target.copy(this.target0),this.object.position.copy(this.position0),this.object.zoom=this.zoom0,this.object.updateProjectionMatrix(),this.dispatchEvent(O0),this.update(),this.state=Zt.NONE}pan(e,t){this._pan(e,t),this.update()}dollyIn(e){this._dollyIn(e),this.update()}dollyOut(e){this._dollyOut(e),this.update()}rotateLeft(e){this._rotateLeft(e),this.update()}rotateUp(e){this._rotateUp(e),this.update()}update(e=null){let t=this.object.position;Dn.copy(t).sub(this.target),Dn.applyQuaternion(this._quat),this._spherical.setFromVector3(Dn),this.autoRotate&&this.state===Zt.NONE&&this._rotateLeft(this._getAutoRotationAngle(e)),this.enableDamping?(this._spherical.theta+=this._sphericalDelta.theta*this.dampingFactor,this._spherical.phi+=this._sphericalDelta.phi*this.dampingFactor):(this._spherical.theta+=this._sphericalDelta.theta,this._spherical.phi+=this._sphericalDelta.phi);let i=this.minAzimuthAngle,s=this.maxAzimuthAngle;isFinite(i)&&isFinite(s)&&(i<-Math.PI?i+=fi:i>Math.PI&&(i-=fi),s<-Math.PI?s+=fi:s>Math.PI&&(s-=fi),i<=s?this._spherical.theta=Math.max(i,Math.min(s,this._spherical.theta)):this._spherical.theta=this._spherical.theta>(i+s)/2?Math.max(i,this._spherical.theta):Math.min(s,this._spherical.theta)),this._spherical.phi=Math.max(this.minPolarAngle,Math.min(this.maxPolarAngle,this._spherical.phi)),this._spherical.makeSafe(),this.enableDamping===!0?this.target.addScaledVector(this._panOffset,this.dampingFactor):this.target.add(this._panOffset),this.target.sub(this.cursor),this.target.clampLength(this.minTargetRadius,this.maxTargetRadius),this.target.add(this.cursor);let r=!1;if(this.zoomToCursor&&this._performCursorZoom||this.object.isOrthographicCamera)this._spherical.radius=this._clampDistance(this._spherical.radius);else{let o=this._spherical.radius;this._spherical.radius=this._clampDistance(this._spherical.radius*this._scale),r=o!=this._spherical.radius}if(Dn.setFromSpherical(this._spherical),Dn.applyQuaternion(this._quatInverse),t.copy(this.target).add(Dn),this.object.lookAt(this.target),this.enableDamping===!0?(this._sphericalDelta.theta*=1-this.dampingFactor,this._sphericalDelta.phi*=1-this.dampingFactor,this._panOffset.multiplyScalar(1-this.dampingFactor)):(this._sphericalDelta.set(0,0,0),this._panOffset.set(0,0,0)),this.zoomToCursor&&this._performCursorZoom){let o=null;if(this.object.isPerspectiveCamera){let a=Dn.length();o=this._clampDistance(a*this._scale);let c=a-o;this.object.position.addScaledVector(this._dollyDirection,c),this.object.updateMatrixWorld(),r=!!c}else if(this.object.isOrthographicCamera){let a=new y(this._mouse.x,this._mouse.y,0);a.unproject(this.object);let c=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),this.object.updateProjectionMatrix(),r=c!==this.object.zoom;let l=new y(this._mouse.x,this._mouse.y,0);l.unproject(this.object),this.object.position.sub(l).add(a),this.object.updateMatrixWorld(),o=Dn.length()}else console.warn("WARNING: OrbitControls.js encountered an unknown camera type - zoom to cursor disabled."),this.zoomToCursor=!1;o!==null&&(this.screenSpacePanning?this.target.set(0,0,-1).transformDirection(this.object.matrix).multiplyScalar(o).add(this.object.position):(fu.origin.copy(this.object.position),fu.direction.set(0,0,-1).transformDirection(this.object.matrix),Math.abs(this.object.up.dot(fu.direction))<jE?this.object.lookAt(this.target):(B0.setFromNormalAndCoplanarPoint(this.object.up,this.target),fu.intersectPlane(B0,this.target))))}else if(this.object.isOrthographicCamera){let o=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),o!==this.object.zoom&&(this.object.updateProjectionMatrix(),r=!0)}return this._scale=1,this._performCursorZoom=!1,r||this._lastPosition.distanceToSquared(this.object.position)>gf||8*(1-this._lastQuaternion.dot(this.object.quaternion))>gf||this._lastTargetPosition.distanceToSquared(this.target)>gf?(this.dispatchEvent(O0),this._lastPosition.copy(this.object.position),this._lastQuaternion.copy(this.object.quaternion),this._lastTargetPosition.copy(this.target),!0):!1}_getAutoRotationAngle(e){return e!==null?fi/60*this.autoRotateSpeed*e:fi/60/60*this.autoRotateSpeed}_getZoomScale(e){let t=Math.abs(e*.01);return Math.pow(.95,this.zoomSpeed*t)}_rotateLeft(e){this._sphericalDelta.theta-=e}_rotateUp(e){this._sphericalDelta.phi-=e}_panLeft(e,t){Dn.setFromMatrixColumn(t,0),Dn.multiplyScalar(-e),this._panOffset.add(Dn)}_panUp(e,t){this.screenSpacePanning===!0?Dn.setFromMatrixColumn(t,1):(Dn.setFromMatrixColumn(t,0),Dn.crossVectors(this.object.up,Dn)),Dn.multiplyScalar(e),this._panOffset.add(Dn)}_pan(e,t){let i=this.domElement;if(this.object.isPerspectiveCamera){let s=this.object.position;Dn.copy(s).sub(this.target);let r=Dn.length();r*=Math.tan(this.object.fov/2*Math.PI/180),this._panLeft(2*e*r/i.clientHeight,this.object.matrix),this._panUp(2*t*r/i.clientHeight,this.object.matrix)}else this.object.isOrthographicCamera?(this._panLeft(e*(this.object.right-this.object.left)/this.object.zoom/i.clientWidth,this.object.matrix),this._panUp(t*(this.object.top-this.object.bottom)/this.object.zoom/i.clientHeight,this.object.matrix)):(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - pan disabled."),this.enablePan=!1)}_dollyOut(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale/=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_dollyIn(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale*=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_updateZoomParameters(e,t){if(!this.zoomToCursor)return;this._performCursorZoom=!0;let i=this.domElement.getBoundingClientRect(),s=e-i.left,r=t-i.top,o=i.width,a=i.height;this._mouse.x=s/o*2-1,this._mouse.y=-(r/a)*2+1,this._dollyDirection.set(this._mouse.x,this._mouse.y,1).unproject(this.object).sub(this.object.position).normalize()}_clampDistance(e){return Math.max(this.minDistance,Math.min(this.maxDistance,e))}_handleMouseDownRotate(e){this._rotateStart.set(e.clientX,e.clientY)}_handleMouseDownDolly(e){this._updateZoomParameters(e.clientX,e.clientX),this._dollyStart.set(e.clientX,e.clientY)}_handleMouseDownPan(e){this._panStart.set(e.clientX,e.clientY)}_handleMouseMoveRotate(e){this._rotateEnd.set(e.clientX,e.clientY),this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(fi*this._rotateDelta.x/t.clientHeight),this._rotateUp(fi*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd),this.update()}_handleMouseMoveDolly(e){this._dollyEnd.set(e.clientX,e.clientY),this._dollyDelta.subVectors(this._dollyEnd,this._dollyStart),this._dollyDelta.y>0?this._dollyOut(this._getZoomScale(this._dollyDelta.y)):this._dollyDelta.y<0&&this._dollyIn(this._getZoomScale(this._dollyDelta.y)),this._dollyStart.copy(this._dollyEnd),this.update()}_handleMouseMovePan(e){this._panEnd.set(e.clientX,e.clientY),this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd),this.update()}_handleMouseWheel(e){this._updateZoomParameters(e.clientX,e.clientY),e.deltaY<0?this._dollyIn(this._getZoomScale(e.deltaY)):e.deltaY>0&&this._dollyOut(this._getZoomScale(e.deltaY)),this.update()}_handleKeyDown(e){let t=!1;switch(e.code){case this.keys.UP:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(fi*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,this.keyPanSpeed),t=!0;break;case this.keys.BOTTOM:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(-fi*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,-this.keyPanSpeed),t=!0;break;case this.keys.LEFT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(fi*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(this.keyPanSpeed,0),t=!0;break;case this.keys.RIGHT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(-fi*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(-this.keyPanSpeed,0),t=!0;break}t&&(e.preventDefault(),this.update())}_handleTouchStartRotate(e){if(this._pointers.length===1)this._rotateStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._rotateStart.set(i,s)}}_handleTouchStartPan(e){if(this._pointers.length===1)this._panStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._panStart.set(i,s)}}_handleTouchStartDolly(e){let t=this._getSecondPointerPosition(e),i=e.pageX-t.x,s=e.pageY-t.y,r=Math.sqrt(i*i+s*s);this._dollyStart.set(0,r)}_handleTouchStartDollyPan(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enablePan&&this._handleTouchStartPan(e)}_handleTouchStartDollyRotate(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enableRotate&&this._handleTouchStartRotate(e)}_handleTouchMoveRotate(e){if(this._pointers.length==1)this._rotateEnd.set(e.pageX,e.pageY);else{let i=this._getSecondPointerPosition(e),s=.5*(e.pageX+i.x),r=.5*(e.pageY+i.y);this._rotateEnd.set(s,r)}this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(fi*this._rotateDelta.x/t.clientHeight),this._rotateUp(fi*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd)}_handleTouchMovePan(e){if(this._pointers.length===1)this._panEnd.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._panEnd.set(i,s)}this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd)}_handleTouchMoveDolly(e){let t=this._getSecondPointerPosition(e),i=e.pageX-t.x,s=e.pageY-t.y,r=Math.sqrt(i*i+s*s);this._dollyEnd.set(0,r),this._dollyDelta.set(0,Math.pow(this._dollyEnd.y/this._dollyStart.y,this.zoomSpeed)),this._dollyOut(this._dollyDelta.y),this._dollyStart.copy(this._dollyEnd);let o=(e.pageX+t.x)*.5,a=(e.pageY+t.y)*.5;this._updateZoomParameters(o,a)}_handleTouchMoveDollyPan(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enablePan&&this._handleTouchMovePan(e)}_handleTouchMoveDollyRotate(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enableRotate&&this._handleTouchMoveRotate(e)}_addPointer(e){this._pointers.push(e.pointerId)}_removePointer(e){delete this._pointerPositions[e.pointerId];for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId){this._pointers.splice(t,1);return}}_isTrackingPointer(e){for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId)return!0;return!1}_trackPointer(e){let t=this._pointerPositions[e.pointerId];t===void 0&&(t=new Pe,this._pointerPositions[e.pointerId]=t),t.set(e.pageX,e.pageY)}_getSecondPointerPosition(e){let t=e.pointerId===this._pointers[0]?this._pointers[1]:this._pointers[0];return this._pointerPositions[t]}_customWheelEvent(e){let t=e.deltaMode,i={clientX:e.clientX,clientY:e.clientY,deltaY:e.deltaY};switch(t){case 1:i.deltaY*=16;break;case 2:i.deltaY*=100;break}return e.ctrlKey&&!this._controlActive&&(i.deltaY*=10),i}};function JE(n){this.enabled!==!1&&(this._pointers.length===0&&(this.domElement.setPointerCapture(n.pointerId),this.domElement.ownerDocument.addEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.addEventListener("pointerup",this._onPointerUp)),!this._isTrackingPointer(n)&&(this._addPointer(n),n.pointerType==="touch"?this._onTouchStart(n):this._onMouseDown(n),this._cursorStyle==="grab"&&(this.domElement.style.cursor="grabbing")))}function QE(n){this.enabled!==!1&&(n.pointerType==="touch"?this._onTouchMove(n):this._onMouseMove(n))}function e1(n){switch(this._removePointer(n),this._pointers.length){case 0:this.domElement.releasePointerCapture(n.pointerId),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.dispatchEvent(H0),this.state=Zt.NONE,this._cursorStyle==="grab"&&(this.domElement.style.cursor="grab");break;case 1:let e=this._pointers[0],t=this._pointerPositions[e];this._onTouchStart({pointerId:e,pageX:t.x,pageY:t.y});break}}function t1(n){let e;switch(n.button){case 0:e=this.mouseButtons.LEFT;break;case 1:e=this.mouseButtons.MIDDLE;break;case 2:e=this.mouseButtons.RIGHT;break;default:e=-1}switch(e){case Ni.DOLLY:if(this.enableZoom===!1)return;this._handleMouseDownDolly(n),this.state=Zt.DOLLY;break;case Ni.ROTATE:if(n.ctrlKey||n.metaKey||n.shiftKey){if(this.enablePan===!1)return;this._handleMouseDownPan(n),this.state=Zt.PAN}else{if(this.enableRotate===!1)return;this._handleMouseDownRotate(n),this.state=Zt.ROTATE}break;case Ni.PAN:if(n.ctrlKey||n.metaKey||n.shiftKey){if(this.enableRotate===!1)return;this._handleMouseDownRotate(n),this.state=Zt.ROTATE}else{if(this.enablePan===!1)return;this._handleMouseDownPan(n),this.state=Zt.PAN}break;default:this.state=Zt.NONE}this.state!==Zt.NONE&&this.dispatchEvent(_f)}function n1(n){switch(this.state){case Zt.ROTATE:if(this.enableRotate===!1)return;this._handleMouseMoveRotate(n);break;case Zt.DOLLY:if(this.enableZoom===!1)return;this._handleMouseMoveDolly(n);break;case Zt.PAN:if(this.enablePan===!1)return;this._handleMouseMovePan(n);break}}function i1(n){this.enabled===!1||this.enableZoom===!1||this.state!==Zt.NONE||(n.preventDefault(),this.dispatchEvent(_f),this._handleMouseWheel(this._customWheelEvent(n)),this.dispatchEvent(H0))}function s1(n){this.enabled!==!1&&this._handleKeyDown(n)}function r1(n){switch(this._trackPointer(n),this._pointers.length){case 1:switch(this.touches.ONE){case ts.ROTATE:if(this.enableRotate===!1)return;this._handleTouchStartRotate(n),this.state=Zt.TOUCH_ROTATE;break;case ts.PAN:if(this.enablePan===!1)return;this._handleTouchStartPan(n),this.state=Zt.TOUCH_PAN;break;default:this.state=Zt.NONE}break;case 2:switch(this.touches.TWO){case ts.DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchStartDollyPan(n),this.state=Zt.TOUCH_DOLLY_PAN;break;case ts.DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchStartDollyRotate(n),this.state=Zt.TOUCH_DOLLY_ROTATE;break;default:this.state=Zt.NONE}break;default:this.state=Zt.NONE}this.state!==Zt.NONE&&this.dispatchEvent(_f)}function o1(n){switch(this._trackPointer(n),this.state){case Zt.TOUCH_ROTATE:if(this.enableRotate===!1)return;this._handleTouchMoveRotate(n),this.update();break;case Zt.TOUCH_PAN:if(this.enablePan===!1)return;this._handleTouchMovePan(n),this.update();break;case Zt.TOUCH_DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchMoveDollyPan(n),this.update();break;case Zt.TOUCH_DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchMoveDollyRotate(n),this.update();break;default:this.state=Zt.NONE}}function a1(n){this.enabled!==!1&&n.preventDefault()}function l1(n){n.key==="Control"&&(this._controlActive=!0,this.domElement.getRootNode().addEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}function c1(n){n.key==="Control"&&(this._controlActive=!1,this.domElement.getRootNode().removeEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}var ga=class n extends dn{constructor(){let e=n.SkyShader,t=new Un({name:e.name,uniforms:ou.clone(e.uniforms),vertexShader:e.vertexShader,fragmentShader:e.fragmentShader,side:Hn,depthWrite:!1});super(new _t(1,1,1),t),this.isSky=!0}};ga.SkyShader={name:"SkyShader",uniforms:{turbidity:{value:2},rayleigh:{value:1},mieCoefficient:{value:.005},mieDirectionalG:{value:.8},sunPosition:{value:new y},cloudScale:{value:2e-4},cloudSpeed:{value:2e-5},cloudCoverage:{value:.4},cloudDensity:{value:.4},cloudElevation:{value:.5},showSunDisc:{value:1},time:{value:0}},vertexShader:`
		uniform vec3 sunPosition;
		uniform float rayleigh;
		uniform float turbidity;
		uniform float mieCoefficient;

		varying vec3 vWorldPosition;
		varying vec3 vSunDirection;
		varying float vSunfade;
		varying vec3 vBetaR;
		varying vec3 vBetaM;
		varying float vSunE;

		// constants for atmospheric scattering
		const float e = 2.71828182845904523536028747135266249775724709369995957;
		const float pi = 3.141592653589793238462643383279502884197169;

		// wavelength of used primaries, according to preetham
		const vec3 lambda = vec3( 680E-9, 550E-9, 450E-9 );
		// this pre-calculation replaces older TotalRayleigh(vec3 lambda) function:
		// (8.0 * pow(pi, 3.0) * pow(pow(n, 2.0) - 1.0, 2.0) * (6.0 + 3.0 * pn)) / (3.0 * N * pow(lambda, vec3(4.0)) * (6.0 - 7.0 * pn))
		const vec3 totalRayleigh = vec3( 5.804542996261093E-6, 1.3562911419845635E-5, 3.0265902468824876E-5 );

		// mie stuff
		// K coefficient for the primaries
		const float v = 4.0;
		const vec3 K = vec3( 0.686, 0.678, 0.666 );
		// MieConst = pi * pow( ( 2.0 * pi ) / lambda, vec3( v - 2.0 ) ) * K
		const vec3 MieConst = vec3( 1.8399918514433978E14, 2.7798023919660528E14, 4.0790479543861094E14 );

		// earth shadow hack
		// cutoffAngle = pi / 1.95;
		const float cutoffAngle = 1.6110731556870734;
		const float steepness = 1.5;
		const float EE = 1000.0;

		float sunIntensity( float zenithAngleCos ) {
			zenithAngleCos = clamp( zenithAngleCos, -1.0, 1.0 );
			return EE * max( 0.0, 1.0 - pow( e, -( ( cutoffAngle - acos( zenithAngleCos ) ) / steepness ) ) );
		}

		vec3 totalMie( float T ) {
			float c = ( 0.2 * T ) * 10E-18;
			return 0.434 * c * MieConst;
		}

		void main() {

			vec4 worldPosition = modelMatrix * vec4( position, 1.0 );
			vWorldPosition = worldPosition.xyz;

			gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			gl_Position.z = gl_Position.w; // set z to camera.far

			vSunDirection = normalize( sunPosition );

			vSunE = sunIntensity( vSunDirection.y );

			vSunfade = 1.0 - clamp( 1.0 - exp( ( sunPosition.y / 450000.0 ) ), 0.0, 1.0 );

			float rayleighCoefficient = rayleigh - ( 1.0 * ( 1.0 - vSunfade ) );

			// extinction (absorption + out scattering)
			// rayleigh coefficients
			vBetaR = totalRayleigh * rayleighCoefficient;

			// mie coefficients
			vBetaM = totalMie( turbidity ) * mieCoefficient;

		}`,fragmentShader:`
		varying vec3 vWorldPosition;
		varying vec3 vSunDirection;
		varying vec3 vBetaR;
		varying vec3 vBetaM;
		varying float vSunE;

		uniform float mieDirectionalG;
		uniform float cloudScale;
		uniform float cloudSpeed;
		uniform float cloudCoverage;
		uniform float cloudDensity;
		uniform float cloudElevation;
		uniform float showSunDisc;
		uniform float time;

		// gradient at a lattice corner; sinless hash so every GPU produces the same clouds
		vec2 gradient( vec2 i ) {
			vec3 p = fract( i.xyx * vec3( 0.1031, 0.1030, 0.0973 ) );
			p += dot( p, p.yzx + 33.33 );
			return fract( ( p.xx + p.yz ) * p.zy ) * 2.0 - 1.0;
		}

		// 2D gradient noise: isotropic lobes like Perlin at value-noise cost
		float noise( vec2 p ) {
			vec2 i = floor( p );
			vec2 f = fract( p );
			vec2 u = f * f * f * ( f * ( f * 6.0 - 15.0 ) + 10.0 ); // quintic fade
			float a = dot( gradient( i ), f );
			float b = dot( gradient( i + vec2( 1.0, 0.0 ) ), f - vec2( 1.0, 0.0 ) );
			float c = dot( gradient( i + vec2( 0.0, 1.0 ) ), f - vec2( 0.0, 1.0 ) );
			float d = dot( gradient( i + vec2( 1.0, 1.0 ) ), f - vec2( 1.0, 1.0 ) );
			return mix( mix( a, b, u.x ), mix( c, d, u.x ), u.y ) * 1.6; // ~[-1,1]
		}

		// fbm; per-octave drift makes clouds billow instead of scrolling as a rigid stamp
		float fbm( vec2 p, float drift ) {
			float result = 0.0;
			float amplitude = 1.0;
			for ( int i = 0; i < 4; i ++ ) {
				result += amplitude * noise( p );
				amplitude *= 0.5;
				p = p * 2.0 + drift;
			}
			return result;
		}

		// constants for atmospheric scattering
		const float pi = 3.141592653589793238462643383279502884197169;

		const float n = 1.0003; // refractive index of air
		const float N = 2.545E25; // number of molecules per unit volume for air at 288.15K and 1013mb (sea level -45 celsius)

		// optical length at zenith for molecules
		const float rayleighZenithLength = 8.4E3;
		const float mieZenithLength = 1.25E3;
		// 66 arc seconds -> degrees, and the cosine of that
		const float sunAngularDiameterCos = 0.999956676946448443553574619906976478926848692873900859324;

		// 3.0 / ( 16.0 * pi )
		const float THREE_OVER_SIXTEENPI = 0.05968310365946075;
		// 1.0 / ( 4.0 * pi )
		const float ONE_OVER_FOURPI = 0.07957747154594767;

		float rayleighPhase( float cosTheta ) {
			return THREE_OVER_SIXTEENPI * ( 1.0 + pow( cosTheta, 2.0 ) );
		}

		float hgPhase( float cosTheta, float g ) {
			float g2 = pow( g, 2.0 );
			float inverse = 1.0 / pow( 1.0 - 2.0 * g * cosTheta + g2, 1.5 );
			return ONE_OVER_FOURPI * ( ( 1.0 - g2 ) * inverse );
		}

		void main() {

			vec3 direction = normalize( vWorldPosition - cameraPosition );

			// optical length
			// cutoff angle at 90 to avoid singularity in next formula.
			float zenithAngle = acos( max( 0.0, direction.y ) );
			float inverse = 1.0 / ( cos( zenithAngle ) + 0.15 * pow( 93.885 - ( ( zenithAngle * 180.0 ) / pi ), -1.253 ) );
			float sR = rayleighZenithLength * inverse;
			float sM = mieZenithLength * inverse;

			// combined extinction factor
			vec3 Fex = exp( -( vBetaR * sR + vBetaM * sM ) );

			// in scattering
			float cosTheta = dot( direction, vSunDirection );

			float rPhase = rayleighPhase( cosTheta * 0.5 + 0.5 );
			vec3 betaRTheta = vBetaR * rPhase;

			float mPhase = hgPhase( cosTheta, mieDirectionalG );
			vec3 betaMTheta = vBetaM * mPhase;

			vec3 Lin = pow( vSunE * ( ( betaRTheta + betaMTheta ) / ( vBetaR + vBetaM ) ) * ( 1.0 - Fex ), vec3( 1.5 ) );
			Lin *= mix( vec3( 1.0 ), pow( vSunE * ( ( betaRTheta + betaMTheta ) / ( vBetaR + vBetaM ) ) * Fex, vec3( 1.0 / 2.0 ) ), clamp( pow( 1.0 - vSunDirection.y, 5.0 ), 0.0, 1.0 ) );

			// nightsky
			float theta = acos( direction.y ); // elevation --> y-axis, [-pi/2, pi/2]
			float phi = atan( direction.z, direction.x ); // azimuth --> x-axis [-pi/2, pi/2]
			vec2 uv = vec2( phi, theta ) / vec2( 2.0 * pi, pi ) + vec2( 0.5, 0.0 );
			vec3 L0 = vec3( 0.1 ) * Fex;

			// composition + solar disc
			float sundisc = clamp( ( cosTheta - sunAngularDiameterCos ) * 50000.0, 0.0, 1.0 ) * showSunDisc;
			vec3 sundiscColor = ( 760.0 * sundisc ) * min( vSunE * Fex, 80.0 );

			vec3 texColor = ( Lin + L0 ) * 0.04 + sundiscColor + vec3( 0.0, 0.0003, 0.00075 );

			// Clouds
			if ( direction.y > 0.0 && cloudCoverage > 0.0 ) {

				// Project to cloud plane (higher elevation = clouds appear lower/closer)
				float elevation = mix( 1.0, 0.1, cloudElevation );
				vec2 cloudUV = direction.xz / ( direction.y * elevation );
				cloudUV *= cloudScale;
				cloudUV += time * cloudSpeed;

				// Cloud density field
				float evolve = time * cloudSpeed * 300.0;
				float cloudNoise = clamp( fbm( cloudUV * 1000.0, evolve ) * 0.7 + 0.5, 0.0, 1.0 );

				// Large-scale coverage variation: clear gaps next to dense banks
				float region = noise( cloudUV * 300.0 ) * 0.37 + 0.5;
				float cov = clamp( cloudCoverage + ( region - 0.5 ) * 0.6, 0.0, 1.0 );

				// Carve clouds where noise rises above the coverage level
				float threshold = 1.0 - cov;
				float cloudMask = smoothstep( threshold, threshold + 0.3, cloudNoise );

				// Fade clouds near horizon (adjusted by elevation)
				float horizonFade = smoothstep( 0.0, 0.03 + 0.06 * cloudElevation, direction.y );
				cloudMask *= horizonFade;

				// Cloud lighting from the sky's own radiance
				float dayFactor = smoothstep( -0.08, 0.3, vSunDirection.y );
				vec3 sunColor = vSunE * Fex * 0.22 * 0.04; // 0.22 ~ albedo/pi, 0.04 = exposure; the aerial composite adds the eye-leg extinction
				vec3 skyAmbient = Lin * 0.04 + vec3( 0.0, 0.0003, 0.00075 );

				// Beer-powder self-shadow from the sampled density
				float depth = max( 0.0, cloudNoise - threshold );
				float beer = exp( depth * -4.0 );
				float powder = 1.0 - beer * beer; // beer*beer == exp(-8*depth)
				float shade = mix( 0.45, 1.0, clamp( beer * powder * 2.6, 0.0, 1.0 ) ); // 2.6 = 1/0.385, normalizes beer*powder peak to 1

				// Henyey-Greenstein forward lobe ( g = 0.7 ): silver lining on rims toward the sun
				float silver = clamp( 0.51 / pow( 1.49 - cosTheta * 1.4, 1.5 ), 0.0, 3.0 ); // 0.51=1-g^2, 1.49=1+g^2, 1.4=2g
				float edge = cloudMask * ( 1.0 - cloudMask ) * 4.0;

				vec3 cloudColor = skyAmbient + sunColor * shade;
				cloudColor += sunColor * silver * edge * 0.6;
				cloudColor *= max( dayFactor, 0.03 );

				// Cloud opacity via Beer's law: density sets how solid the clouds get
				float alpha = ( 1.0 - exp( depth * cloudDensity * -12.0 ) ) * horizonFade;

				// Occlude the sun disc/glow behind opaque cloud
				texColor -= L0 * 0.04 * alpha;

				// Composite through the atmosphere so distant clouds dissolve into haze
				vec3 cloudAerial = mix( texColor, cloudColor, Fex );
				texColor = mix( texColor, cloudAerial, alpha );

			}

			gl_FragColor = vec4( texColor, 1.0 );

			#include <tonemapping_fragment>
			#include <colorspace_fragment>

		}`};var Dl=new y;function Fi(n,e,t,i,s,r){let o=2*Math.PI*s/4,a=Math.max(r-2*s,0),c=Math.PI/4;Dl.copy(e),Dl[i]=0,Dl.normalize();let l=.5*o/(o+a),u=1-Dl.angleTo(n)/c;return Math.sign(Dl[t])===1?u*l:a/(o+a)+l+l*(1-u)}var mu=class n extends _t{constructor(e=1,t=1,i=1,s=2,r=.1){let o=s*2+1;if(r=Math.min(e/2,t/2,i/2,r),super(1,1,1,o,o,o),this.type="RoundedBoxGeometry",this.parameters={width:e,height:t,depth:i,segments:s,radius:r},o===1)return;let a=this.toNonIndexed();this.index=null,this.attributes.position=a.attributes.position,this.attributes.normal=a.attributes.normal,this.attributes.uv=a.attributes.uv;let c=new y,l=new y,u=new y(e,t,i).divideScalar(2).subScalar(r),d=this.attributes.position.array,f=this.attributes.normal.array,p=this.attributes.uv.array,x=d.length/6,b=new y,g=.5/o;for(let m=0,A=0;m<d.length;m+=3,A+=2)switch(c.fromArray(d,m),l.copy(c),l.x-=Math.sign(l.x)*g,l.y-=Math.sign(l.y)*g,l.z-=Math.sign(l.z)*g,l.normalize(),d[m+0]=u.x*Math.sign(c.x)+l.x*r,d[m+1]=u.y*Math.sign(c.y)+l.y*r,d[m+2]=u.z*Math.sign(c.z)+l.z*r,f[m+0]=l.x,f[m+1]=l.y,f[m+2]=l.z,Math.floor(m/x)){case 0:b.set(1,0,0),p[A+0]=Fi(b,l,"z","y",r,i),p[A+1]=1-Fi(b,l,"y","z",r,t);break;case 1:b.set(-1,0,0),p[A+0]=1-Fi(b,l,"z","y",r,i),p[A+1]=1-Fi(b,l,"y","z",r,t);break;case 2:b.set(0,1,0),p[A+0]=1-Fi(b,l,"x","z",r,e),p[A+1]=Fi(b,l,"z","x",r,i);break;case 3:b.set(0,-1,0),p[A+0]=1-Fi(b,l,"x","z",r,e),p[A+1]=1-Fi(b,l,"z","x",r,i);break;case 4:b.set(0,0,1),p[A+0]=1-Fi(b,l,"x","y",r,e),p[A+1]=1-Fi(b,l,"y","x",r,t);break;case 5:b.set(0,0,-1),p[A+0]=Fi(b,l,"x","y",r,e),p[A+1]=1-Fi(b,l,"y","x",r,t);break}}static fromJSON(e){return new n(e.width,e.height,e.depth,e.segments,e.radius)}};function xf(n,e){if(e===Wd)return console.warn("THREE.BufferGeometryUtils.toTrianglesDrawMode(): Geometry already defined as triangles."),n;if(e===ha||e===Cl){let t=n.getIndex();if(t===null){let r=[],o=n.getAttribute("position");if(o!==void 0){for(let a=0;a<o.count;a++)r.push(a);n.setIndex(r),t=n.getIndex()}else return console.error("THREE.BufferGeometryUtils.toTrianglesDrawMode(): Undefined position attribute. Processing not possible."),n}let i=t.count-2,s=[];if(e===ha)for(let r=1;r<=i;r++)s.push(t.getX(0)),s.push(t.getX(r)),s.push(t.getX(r+1));else for(let r=0;r<i;r++)r%2===0?(s.push(t.getX(r)),s.push(t.getX(r+1)),s.push(t.getX(r+2))):(s.push(t.getX(r+2)),s.push(t.getX(r+1)),s.push(t.getX(r)));return s.length/3!==i&&console.error("THREE.BufferGeometryUtils.toTrianglesDrawMode(): Unable to generate correct amount of triangles."),n.setIndex(s),n.clearGroups(),n}else return console.error("THREE.BufferGeometryUtils.toTrianglesDrawMode(): Unknown draw mode:",e),n}function k0(n){let e=new Map,t=new Map,i=n.clone();return V0(n,i,function(s,r){e.set(r,s),t.set(s,r)}),i.traverse(function(s){if(!s.isSkinnedMesh)return;let r=s,o=e.get(s),a=o.skeleton.bones;r.skeleton=o.skeleton.clone(),r.bindMatrix.copy(o.bindMatrix),r.skeleton.bones=a.map(function(c){return t.get(c)}),r.bind(r.skeleton,r.bindMatrix)}),i}function V0(n,e,t){t(n,e);for(let i=0;i<n.children.length;i++)V0(n.children[i],e.children[i],t)}var gu=class extends Ms{constructor(e){super(e),this.dracoLoader=null,this.ktx2Loader=null,this.meshoptDecoder=null,this.pluginCallbacks=[],this.register(function(t){return new Sf(t)}),this.register(function(t){return new wf(t)}),this.register(function(t){return new Uf(t)}),this.register(function(t){return new Ff(t)}),this.register(function(t){return new Of(t)}),this.register(function(t){return new Rf(t)}),this.register(function(t){return new Cf(t)}),this.register(function(t){return new If(t)}),this.register(function(t){return new Pf(t)}),this.register(function(t){return new Tf(t)}),this.register(function(t){return new Lf(t)}),this.register(function(t){return new Af(t)}),this.register(function(t){return new Nf(t)}),this.register(function(t){return new Df(t)}),this.register(function(t){return new Ef(t)}),this.register(function(t){return new _u(t,Lt.EXT_MESHOPT_COMPRESSION)}),this.register(function(t){return new _u(t,Lt.KHR_MESHOPT_COMPRESSION)}),this.register(function(t){return new Bf(t)})}load(e,t,i,s){let r=this,o;if(this.resourcePath!=="")o=this.resourcePath;else if(this.path!==""){let l=Ys.extractUrlBase(e);o=Ys.resolveURL(l,this.path)}else o=Ys.extractUrlBase(e);this.manager.itemStart(e);let a=function(l){s?s(l):console.error(l),r.manager.itemError(e),r.manager.itemEnd(e)},c=new na(this.manager);c.setPath(this.path),c.setResponseType("arraybuffer"),c.setRequestHeader(this.requestHeader),c.setWithCredentials(this.withCredentials),c.load(e,function(l){try{r.parse(l,o,function(u){t(u),r.manager.itemEnd(e)},a)}catch(u){a(u)}},i,a)}setDRACOLoader(e){return this.dracoLoader=e,this}setKTX2Loader(e){return this.ktx2Loader=e,this}setMeshoptDecoder(e){return this.meshoptDecoder=e,this}register(e){return this.pluginCallbacks.indexOf(e)===-1&&this.pluginCallbacks.push(e),this}unregister(e){return this.pluginCallbacks.indexOf(e)!==-1&&this.pluginCallbacks.splice(this.pluginCallbacks.indexOf(e),1),this}parse(e,t,i,s){let r,o={},a={},c=new TextDecoder;if(typeof e=="string")r=JSON.parse(e);else if(e instanceof ArrayBuffer)if(c.decode(new Uint8Array(e,0,4))===q0){try{o[Lt.KHR_BINARY_GLTF]=new Hf(e)}catch(d){s&&s(d);return}r=JSON.parse(o[Lt.KHR_BINARY_GLTF].content)}else r=JSON.parse(c.decode(e));else r=e;if(r.asset===void 0||r.asset.version[0]<2){s&&s(new Error("THREE.GLTFLoader: Unsupported asset. glTF versions >=2.0 are supported."));return}let l=new qf(r,{path:t||this.resourcePath||"",crossOrigin:this.crossOrigin,requestHeader:this.requestHeader,manager:this.manager,ktx2Loader:this.ktx2Loader,meshoptDecoder:this.meshoptDecoder});l.fileLoader.setRequestHeader(this.requestHeader);for(let u=0;u<this.pluginCallbacks.length;u++){let d=this.pluginCallbacks[u](l);d.name||console.error("THREE.GLTFLoader: Invalid plugin found: missing name"),a[d.name]=d,o[d.name]=!0}if(r.extensionsUsed)for(let u=0;u<r.extensionsUsed.length;++u){let d=r.extensionsUsed[u],f=r.extensionsRequired||[];switch(d){case Lt.KHR_MATERIALS_UNLIT:o[d]=new bf;break;case Lt.KHR_DRACO_MESH_COMPRESSION:o[d]=new kf(r,this.dracoLoader);break;case Lt.KHR_TEXTURE_TRANSFORM:o[d]=new Vf;break;case Lt.KHR_MESH_QUANTIZATION:o[d]=new zf;break;default:f.indexOf(d)>=0&&a[d]===void 0&&console.warn('THREE.GLTFLoader: Unknown extension "'+d+'".')}}l.setExtensions(o),l.setPlugins(a),l.parse(i,s)}parseAsync(e,t){let i=this;return new Promise(function(s,r){i.parse(e,t,s,r)})}};function h1(){let n={};return{get:function(e){return n[e]},add:function(e,t){n[e]=t},remove:function(e){delete n[e]},removeAll:function(){n={}}}}function Mn(n,e,t){let i=n.json.materials[e];return i.extensions&&i.extensions[t]?i.extensions[t]:null}var Lt={KHR_BINARY_GLTF:"KHR_binary_glTF",KHR_DRACO_MESH_COMPRESSION:"KHR_draco_mesh_compression",KHR_LIGHTS_PUNCTUAL:"KHR_lights_punctual",KHR_MATERIALS_CLEARCOAT:"KHR_materials_clearcoat",KHR_MATERIALS_DISPERSION:"KHR_materials_dispersion",KHR_MATERIALS_IOR:"KHR_materials_ior",KHR_MATERIALS_SHEEN:"KHR_materials_sheen",KHR_MATERIALS_SPECULAR:"KHR_materials_specular",KHR_MATERIALS_TRANSMISSION:"KHR_materials_transmission",KHR_MATERIALS_IRIDESCENCE:"KHR_materials_iridescence",KHR_MATERIALS_ANISOTROPY:"KHR_materials_anisotropy",KHR_MATERIALS_UNLIT:"KHR_materials_unlit",KHR_MATERIALS_VOLUME:"KHR_materials_volume",KHR_TEXTURE_BASISU:"KHR_texture_basisu",KHR_TEXTURE_TRANSFORM:"KHR_texture_transform",KHR_MESH_QUANTIZATION:"KHR_mesh_quantization",KHR_MATERIALS_EMISSIVE_STRENGTH:"KHR_materials_emissive_strength",EXT_MATERIALS_BUMP:"EXT_materials_bump",EXT_TEXTURE_WEBP:"EXT_texture_webp",EXT_TEXTURE_AVIF:"EXT_texture_avif",EXT_MESHOPT_COMPRESSION:"EXT_meshopt_compression",KHR_MESHOPT_COMPRESSION:"KHR_meshopt_compression",EXT_MESH_GPU_INSTANCING:"EXT_mesh_gpu_instancing"},Ef=class{constructor(e){this.parser=e,this.name=Lt.KHR_LIGHTS_PUNCTUAL,this.cache={refs:{},uses:{}}}_markDefs(){let e=this.parser,t=this.parser.json.nodes||[];for(let i=0,s=t.length;i<s;i++){let r=t[i];r.extensions&&r.extensions[this.name]&&r.extensions[this.name].light!==void 0&&e._addNodeRef(this.cache,r.extensions[this.name].light)}}_loadLight(e){let t=this.parser,i="light:"+e,s=t.cache.get(i);if(s)return s;let r=t.json,c=((r.extensions&&r.extensions[this.name]||{}).lights||[])[e],l,u=new ke(16777215);c.color!==void 0&&u.setRGB(c.color[0],c.color[1],c.color[2],ti);let d=c.range!==void 0?c.range:0;switch(c.type){case"directional":l=new Qr(u),l.target.position.set(0,0,-1),l.add(l.target);break;case"point":l=new Di(u),l.distance=d;break;case"spot":l=new ml(u),l.distance=d,c.spot=c.spot||{},c.spot.innerConeAngle=c.spot.innerConeAngle!==void 0?c.spot.innerConeAngle:0,c.spot.outerConeAngle=c.spot.outerConeAngle!==void 0?c.spot.outerConeAngle:Math.PI/4,l.angle=c.spot.outerConeAngle,l.penumbra=1-c.spot.innerConeAngle/c.spot.outerConeAngle,l.target.position.set(0,0,-1),l.add(l.target);break;default:throw new Error("THREE.GLTFLoader: Unexpected light type: "+c.type)}return l.position.set(0,0,0),ws(l,c),c.intensity!==void 0&&(l.intensity=c.intensity),l.name=t.createUniqueName(c.name||"light_"+e),s=Promise.resolve(l),t.cache.add(i,s),s}getDependency(e,t){if(e==="light")return this._loadLight(t)}createNodeAttachment(e){let t=this,i=this.parser,r=i.json.nodes[e],a=(r.extensions&&r.extensions[this.name]||{}).light;return a===void 0?null:this._loadLight(a).then(function(c){return i._getNodeRef(t.cache,a,c)})}},bf=class{constructor(){this.name=Lt.KHR_MATERIALS_UNLIT}getMaterialType(){return ln}extendParams(e,t,i){let s=[];e.color=new ke(1,1,1),e.opacity=1;let r=t.pbrMetallicRoughness;if(r){if(Array.isArray(r.baseColorFactor)){let o=r.baseColorFactor;e.color.setRGB(o[0],o[1],o[2],ti),e.opacity=o[3]}r.baseColorTexture!==void 0&&s.push(i.assignTexture(e,"map",r.baseColorTexture,sn))}return Promise.all(s)}},Tf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_EMISSIVE_STRENGTH}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);return i===null||i.emissiveStrength!==void 0&&(t.emissiveIntensity=i.emissiveStrength),Promise.resolve()}},Sf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_CLEARCOAT}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];if(i.clearcoatFactor!==void 0&&(t.clearcoat=i.clearcoatFactor),i.clearcoatTexture!==void 0&&s.push(this.parser.assignTexture(t,"clearcoatMap",i.clearcoatTexture)),i.clearcoatRoughnessFactor!==void 0&&(t.clearcoatRoughness=i.clearcoatRoughnessFactor),i.clearcoatRoughnessTexture!==void 0&&s.push(this.parser.assignTexture(t,"clearcoatRoughnessMap",i.clearcoatRoughnessTexture)),i.clearcoatNormalTexture!==void 0&&(s.push(this.parser.assignTexture(t,"clearcoatNormalMap",i.clearcoatNormalTexture)),i.clearcoatNormalTexture.scale!==void 0)){let r=i.clearcoatNormalTexture.scale;t.clearcoatNormalScale=new Pe(r,r)}return Promise.all(s)}},wf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_DISPERSION}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);return i===null||(t.dispersion=i.dispersion!==void 0?i.dispersion:0),Promise.resolve()}},Af=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_IRIDESCENCE}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];return i.iridescenceFactor!==void 0&&(t.iridescence=i.iridescenceFactor),i.iridescenceTexture!==void 0&&s.push(this.parser.assignTexture(t,"iridescenceMap",i.iridescenceTexture)),i.iridescenceIor!==void 0&&(t.iridescenceIOR=i.iridescenceIor),t.iridescenceThicknessRange===void 0&&(t.iridescenceThicknessRange=[100,400]),i.iridescenceThicknessMinimum!==void 0&&(t.iridescenceThicknessRange[0]=i.iridescenceThicknessMinimum),i.iridescenceThicknessMaximum!==void 0&&(t.iridescenceThicknessRange[1]=i.iridescenceThicknessMaximum),i.iridescenceThicknessTexture!==void 0&&s.push(this.parser.assignTexture(t,"iridescenceThicknessMap",i.iridescenceThicknessTexture)),Promise.all(s)}},Rf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_SHEEN}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];if(t.sheenColor=new ke(0,0,0),t.sheenRoughness=0,t.sheen=1,i.sheenColorFactor!==void 0){let r=i.sheenColorFactor;t.sheenColor.setRGB(r[0],r[1],r[2],ti)}return i.sheenRoughnessFactor!==void 0&&(t.sheenRoughness=i.sheenRoughnessFactor),i.sheenColorTexture!==void 0&&s.push(this.parser.assignTexture(t,"sheenColorMap",i.sheenColorTexture,sn)),i.sheenRoughnessTexture!==void 0&&s.push(this.parser.assignTexture(t,"sheenRoughnessMap",i.sheenRoughnessTexture)),Promise.all(s)}},Cf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_TRANSMISSION}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];return i.transmissionFactor!==void 0&&(t.transmission=i.transmissionFactor),i.transmissionTexture!==void 0&&s.push(this.parser.assignTexture(t,"transmissionMap",i.transmissionTexture)),Promise.all(s)}},If=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_VOLUME}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];t.thickness=i.thicknessFactor!==void 0?i.thicknessFactor:0,i.thicknessTexture!==void 0&&s.push(this.parser.assignTexture(t,"thicknessMap",i.thicknessTexture)),t.attenuationDistance=i.attenuationDistance||1/0;let r=i.attenuationColor||[1,1,1];return t.attenuationColor=new ke().setRGB(r[0],r[1],r[2],ti),Promise.all(s)}},Pf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_IOR}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);return i===null||(t.ior=i.ior!==void 0?i.ior:1.5,t.ior===0&&(t.ior=1e3)),Promise.resolve()}},Lf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_SPECULAR}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];t.specularIntensity=i.specularFactor!==void 0?i.specularFactor:1,i.specularTexture!==void 0&&s.push(this.parser.assignTexture(t,"specularIntensityMap",i.specularTexture));let r=i.specularColorFactor||[1,1,1];return t.specularColor=new ke().setRGB(r[0],r[1],r[2],ti),i.specularColorTexture!==void 0&&s.push(this.parser.assignTexture(t,"specularColorMap",i.specularColorTexture,sn)),Promise.all(s)}},Df=class{constructor(e){this.parser=e,this.name=Lt.EXT_MATERIALS_BUMP}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];return t.bumpScale=i.bumpFactor!==void 0?i.bumpFactor:1,i.bumpTexture!==void 0&&s.push(this.parser.assignTexture(t,"bumpMap",i.bumpTexture)),Promise.all(s)}},Nf=class{constructor(e){this.parser=e,this.name=Lt.KHR_MATERIALS_ANISOTROPY}getMaterialType(e){return Mn(this.parser,e,this.name)!==null?hi:null}extendMaterialParams(e,t){let i=Mn(this.parser,e,this.name);if(i===null)return Promise.resolve();let s=[];return i.anisotropyStrength!==void 0&&(t.anisotropy=i.anisotropyStrength),i.anisotropyRotation!==void 0&&(t.anisotropyRotation=i.anisotropyRotation),i.anisotropyTexture!==void 0&&s.push(this.parser.assignTexture(t,"anisotropyMap",i.anisotropyTexture)),Promise.all(s)}},Uf=class{constructor(e){this.parser=e,this.name=Lt.KHR_TEXTURE_BASISU}loadTexture(e){let t=this.parser,i=t.json,s=i.textures[e];if(!s.extensions||!s.extensions[this.name])return null;let r=s.extensions[this.name],o=t.options.ktx2Loader;if(!o){if(i.extensionsRequired&&i.extensionsRequired.indexOf(this.name)>=0)throw new Error("THREE.GLTFLoader: setKTX2Loader must be called before loading KTX2 textures");return null}return t.loadTextureImage(e,r.source,o)}},Ff=class{constructor(e){this.parser=e,this.name=Lt.EXT_TEXTURE_WEBP}loadTexture(e){let t=this.name,i=this.parser,s=i.json,r=s.textures[e];if(!r.extensions||!r.extensions[t])return null;let o=r.extensions[t],a=s.images[o.source],c=i.textureLoader;if(a.uri){let l=i.options.manager.getHandler(a.uri);l!==null&&(c=l)}return i.loadTextureImage(e,o.source,c)}},Of=class{constructor(e){this.parser=e,this.name=Lt.EXT_TEXTURE_AVIF}loadTexture(e){let t=this.name,i=this.parser,s=i.json,r=s.textures[e];if(!r.extensions||!r.extensions[t])return null;let o=r.extensions[t],a=s.images[o.source],c=i.textureLoader;if(a.uri){let l=i.options.manager.getHandler(a.uri);l!==null&&(c=l)}return i.loadTextureImage(e,o.source,c)}},_u=class{constructor(e,t){this.name=t,this.parser=e}loadBufferView(e){let t=this.parser.json,i=t.bufferViews[e];if(i.extensions&&i.extensions[this.name]){let s=i.extensions[this.name],r=this.parser.getDependency("buffer",s.buffer),o=this.parser.options.meshoptDecoder;if(!o||!o.supported){if(t.extensionsRequired&&t.extensionsRequired.indexOf(this.name)>=0)throw new Error("THREE.GLTFLoader: setMeshoptDecoder must be called before loading compressed files");return null}return r.then(function(a){let c=s.byteOffset||0,l=s.byteLength||0,u=s.count,d=s.byteStride,f=new Uint8Array(a,c,l);return o.decodeGltfBufferAsync?o.decodeGltfBufferAsync(u,d,f,s.mode,s.filter).then(function(p){return p.buffer}):o.ready.then(function(){let p=new ArrayBuffer(u*d);return o.decodeGltfBuffer(new Uint8Array(p),u,d,f,s.mode,s.filter),p})})}else return null}},Bf=class{constructor(e){this.name=Lt.EXT_MESH_GPU_INSTANCING,this.parser=e}createNodeMesh(e){let t=this.parser.json,i=t.nodes[e];if(!i.extensions||!i.extensions[this.name]||i.mesh===void 0)return null;let s=t.meshes[i.mesh];for(let l of s.primitives)if(l.mode!==Oi.TRIANGLES&&l.mode!==Oi.TRIANGLE_STRIP&&l.mode!==Oi.TRIANGLE_FAN&&l.mode!==void 0)return null;let o=i.extensions[this.name].attributes,a=[],c={};for(let l in o)a.push(this.parser.getDependency("accessor",o[l]).then(u=>(c[l]=u,c[l])));return a.length<1?null:(a.push(this.parser.createNodeMesh(e)),Promise.all(a).then(l=>{let u=l.pop(),d=u.isGroup?u.children:[u],f=l[0].count,p=[];for(let x of d){let b=new rt,g=new y,m=new rn,A=new y(1,1,1),U=new ii(x.geometry,x.material,f);for(let I=0;I<f;I++)c.TRANSLATION&&g.fromBufferAttribute(c.TRANSLATION,I),c.ROTATION&&m.fromBufferAttribute(c.ROTATION,I),c.SCALE&&A.fromBufferAttribute(c.SCALE,I),U.setMatrixAt(I,b.compose(g,m,A));let T=null;for(let I in c)if(I==="_COLOR_0"){let L=c[I];U.instanceColor=new Vs(L.array,L.itemSize,L.normalized)}else if(I!=="TRANSLATION"&&I!=="ROTATION"&&I!=="SCALE"){if(T===null){let P=U.geometry;T=new tn,T.name=P.name;for(let M in P.attributes)T.setAttribute(M,P.attributes[M]);for(let M in P.morphAttributes)T.morphAttributes[M]=P.morphAttributes[M];P.index!==null&&T.setIndex(P.index),T.morphTargetsRelative=P.morphTargetsRelative;for(let M of P.groups)T.addGroup(M.start,M.count,M.materialIndex);P.boundingBox!==null&&(T.boundingBox=P.boundingBox.clone()),P.boundingSphere!==null&&(T.boundingSphere=P.boundingSphere.clone()),T.drawRange.start=P.drawRange.start,T.drawRange.count=P.drawRange.count,T.userData=Object.assign({},P.userData),U.geometry=T}let L=c[I];T.setAttribute(I,new Vs(L.array,L.itemSize,L.normalized))}an.prototype.copy.call(U,x),this.parser.assignFinalMaterial(U),p.push(U)}return u.isGroup?(u.clear(),u.add(...p),u):p[0]}))}},q0="glTF",Nl=12,z0={JSON:1313821514,BIN:5130562},Hf=class{constructor(e){this.name=Lt.KHR_BINARY_GLTF,this.content=null,this.body=null;let t=new DataView(e,0,Nl),i=new TextDecoder;if(this.header={magic:i.decode(new Uint8Array(e.slice(0,4))),version:t.getUint32(4,!0),length:t.getUint32(8,!0)},this.header.magic!==q0)throw new Error("THREE.GLTFLoader: Unsupported glTF-Binary header.");if(this.header.version<2)throw new Error("THREE.GLTFLoader: Legacy binary file detected.");let s=this.header.length-Nl,r=new DataView(e,Nl),o=0;for(;o<s;){let a=r.getUint32(o,!0);o+=4;let c=r.getUint32(o,!0);if(o+=4,c===z0.JSON){let l=new Uint8Array(e,Nl+o,a);this.content=i.decode(l)}else if(c===z0.BIN){let l=Nl+o;this.body=e.slice(l,l+a)}o+=a}if(this.content===null)throw new Error("THREE.GLTFLoader: JSON content not found.")}},kf=class{constructor(e,t){if(!t)throw new Error("THREE.GLTFLoader: No DRACOLoader instance provided.");this.name=Lt.KHR_DRACO_MESH_COMPRESSION,this.json=e,this.dracoLoader=t,this.dracoLoader.preload()}decodePrimitive(e,t){let i=this.json,s=this.dracoLoader,r=e.extensions[this.name].bufferView,o=e.extensions[this.name].attributes,a={},c={},l={};for(let u in o){let d=Wf[u]||u.toLowerCase();a[d]=o[u]}for(let u in e.attributes){let d=Wf[u]||u.toLowerCase();if(o[u]!==void 0){let f=i.accessors[e.attributes[u]],p=_a[f.componentType];l[d]=p.name,c[d]=f.normalized===!0}}return t.getDependency("bufferView",r).then(function(u){return new Promise(function(d,f){s.decodeDracoFile(u,function(p){for(let x in p.attributes){let b=p.attributes[x],g=c[x];g!==void 0&&(b.normalized=g)}d(p)},a,l,ti,f)})})}},Vf=class{constructor(){this.name=Lt.KHR_TEXTURE_TRANSFORM}extendTexture(e,t){if((t.texCoord===void 0||t.texCoord===e.channel)&&t.offset===void 0&&t.rotation===void 0&&t.scale===void 0)return e;if(e=e.clone(),t.texCoord!==void 0&&(e.channel=t.texCoord),t.offset!==void 0&&e.offset.fromArray(t.offset),t.rotation!==void 0&&(e.rotation=t.rotation),t.scale!==void 0&&e.repeat.fromArray(t.scale),t.rotation!==void 0){let i=Math.cos(e.rotation),s=Math.sin(e.rotation);e.matrix.set(e.repeat.x*i,e.repeat.y*s,e.offset.x,-e.repeat.x*s,e.repeat.y*i,e.offset.y,0,0,1),e.matrixAutoUpdate=!1}return e.needsUpdate=!0,e}},zf=class{constructor(){this.name=Lt.KHR_MESH_QUANTIZATION}},xu=class extends ys{constructor(e,t,i,s){super(e,t,i,s)}copySampleValue_(e){let t=this.resultBuffer,i=this.sampleValues,s=this.valueSize,r=e*s*3+s;for(let o=0;o!==s;o++)t[o]=i[r+o];return t}interpolate_(e,t,i,s){let r=this.resultBuffer,o=this.sampleValues,a=this.valueSize,c=a*2,l=a*3,u=s-t,d=(i-t)/u,f=d*d,p=f*d,x=e*l,b=x-l,g=-2*p+3*f,m=p-f,A=1-g,U=m-f+d;for(let T=0;T!==a;T++){let I=o[b+T+a],L=o[b+T+c]*u,P=o[x+T+a],M=o[x+T]*u;r[T]=A*I+U*L+g*P+m*M}return r}},u1=new rn,Gf=class extends xu{interpolate_(e,t,i,s){let r=super.interpolate_(e,t,i,s);return u1.fromArray(r).normalize().toArray(r),r}},Oi={FLOAT:5126,FLOAT_MAT3:35675,FLOAT_MAT4:35676,FLOAT_VEC2:35664,FLOAT_VEC3:35665,FLOAT_VEC4:35666,LINEAR:9729,REPEAT:10497,SAMPLER_2D:35678,POINTS:0,LINES:1,LINE_LOOP:2,LINE_STRIP:3,TRIANGLES:4,TRIANGLE_STRIP:5,TRIANGLE_FAN:6,UNSIGNED_BYTE:5121,UNSIGNED_SHORT:5123},_a={5120:Int8Array,5121:Uint8Array,5122:Int16Array,5123:Uint16Array,5125:Uint32Array,5126:Float32Array},G0={9728:vn,9729:yn,9984:vh,9985:aa,9986:no,9987:is},W0={33071:Ii,33648:Wo,10497:oi},vf={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT2:4,MAT3:9,MAT4:16},Wf={POSITION:"position",NORMAL:"normal",TANGENT:"tangent",TEXCOORD_0:"uv",TEXCOORD_1:"uv1",TEXCOORD_2:"uv2",TEXCOORD_3:"uv3",COLOR_0:"color",WEIGHTS_0:"skinWeight",JOINTS_0:"skinIndex"},vr={scale:"scale",translation:"position",rotation:"quaternion",weights:"morphTargetInfluences"},d1={CUBICSPLINE:void 0,LINEAR:zr,STEP:Vr},yf={OPAQUE:"OPAQUE",MASK:"MASK",BLEND:"BLEND"};function f1(n){return n.DefaultMaterial===void 0&&(n.DefaultMaterial=new ge({color:16777215,emissive:0,metalness:1,roughness:1,transparent:!1,depthTest:!0,side:Es})),n.DefaultMaterial}function ro(n,e,t){for(let i in t.extensions)n[i]===void 0&&(e.userData.gltfExtensions=e.userData.gltfExtensions||{},e.userData.gltfExtensions[i]=t.extensions[i])}function ws(n,e){e.extras!==void 0&&(typeof e.extras=="object"?Object.assign(n.userData,e.extras):console.warn("THREE.GLTFLoader: Ignoring primitive type .extras, "+e.extras))}function p1(n,e,t){let i=!1,s=!1,r=!1;for(let l=0,u=e.length;l<u;l++){let d=e[l];if(d.POSITION!==void 0&&(i=!0),d.NORMAL!==void 0&&(s=!0),d.COLOR_0!==void 0&&(r=!0),i&&s&&r)break}if(!i&&!s&&!r)return Promise.resolve(n);let o=[],a=[],c=[];for(let l=0,u=e.length;l<u;l++){let d=e[l];if(i){let f=d.POSITION!==void 0?t.getDependency("accessor",d.POSITION):n.attributes.position;o.push(f)}if(s){let f=d.NORMAL!==void 0?t.getDependency("accessor",d.NORMAL):n.attributes.normal;a.push(f)}if(r){let f=d.COLOR_0!==void 0?t.getDependency("accessor",d.COLOR_0):n.attributes.color;c.push(f)}}return Promise.all([Promise.all(o),Promise.all(a),Promise.all(c)]).then(function(l){let u=l[0],d=l[1],f=l[2];return i&&(n.morphAttributes.position=u),s&&(n.morphAttributes.normal=d),r&&(n.morphAttributes.color=f),n.morphTargetsRelative=!0,n})}function m1(n,e){if(n.updateMorphTargets(),e.weights!==void 0)for(let t=0,i=e.weights.length;t<i;t++)n.morphTargetInfluences[t]=e.weights[t];if(e.extras&&Array.isArray(e.extras.targetNames)){let t=e.extras.targetNames;if(n.morphTargetInfluences.length===t.length){n.morphTargetDictionary={};for(let i=0,s=t.length;i<s;i++)n.morphTargetDictionary[t[i]]=i}else console.warn("THREE.GLTFLoader: Invalid extras.targetNames length. Ignoring names.")}}function g1(n){let e,t=n.extensions&&n.extensions[Lt.KHR_DRACO_MESH_COMPRESSION];if(t?e="draco:"+t.bufferView+":"+t.indices+":"+Mf(t.attributes):e=n.indices+":"+Mf(n.attributes)+":"+n.mode,n.targets!==void 0)for(let i=0,s=n.targets.length;i<s;i++)e+=":"+Mf(n.targets[i]);return e}function Mf(n){let e="",t=Object.keys(n).sort();for(let i=0,s=t.length;i<s;i++)e+=t[i]+":"+n[t[i]]+";";return e}function Xf(n){switch(n){case Int8Array:return 1/127;case Uint8Array:return 1/255;case Int16Array:return 1/32767;case Uint16Array:return 1/65535;default:throw new Error("THREE.GLTFLoader: Unsupported normalized accessor component type.")}}function _1(n){return n.search(/\.jpe?g($|\?)/i)>0||n.search(/^data\:image\/jpeg/)===0?"image/jpeg":n.search(/\.webp($|\?)/i)>0||n.search(/^data\:image\/webp/)===0?"image/webp":n.search(/\.ktx2($|\?)/i)>0||n.search(/^data\:image\/ktx2/)===0?"image/ktx2":"image/png"}var x1=new rt,qf=class{constructor(e={},t={}){this.json=e,this.extensions={},this.plugins={},this.options=t,this.cache=new h1,this.associations=new Map,this.primitiveCache={},this.nodeCache={},this.meshCache={refs:{},uses:{}},this.cameraCache={refs:{},uses:{}},this.lightCache={refs:{},uses:{}},this.sourceCache={},this.textureCache={},this.nodeNamesUsed={};let i=!1,s=-1,r=!1,o=-1;if(typeof navigator<"u"&&typeof navigator.userAgent<"u"){let a=navigator.userAgent;i=/^((?!chrome|android).)*safari/i.test(a)===!0;let c=a.match(/Version\/(\d+)/);s=i&&c?parseInt(c[1],10):-1,r=a.indexOf("Firefox")>-1,o=r?a.match(/Firefox\/([0-9]+)\./)[1]:-1}typeof createImageBitmap>"u"||i&&s<17||r&&o<98?this.textureLoader=new dl(this.options.manager):this.textureLoader=new gl(this.options.manager),this.textureLoader.setCrossOrigin(this.options.crossOrigin),this.textureLoader.setRequestHeader(this.options.requestHeader),this.fileLoader=new na(this.options.manager),this.fileLoader.setResponseType("arraybuffer"),this.options.crossOrigin==="use-credentials"&&this.fileLoader.setWithCredentials(!0)}setExtensions(e){this.extensions=e}setPlugins(e){this.plugins=e}parse(e,t){let i=this,s=this.json,r=this.extensions;this.cache.removeAll(),this.nodeCache={},this._invokeAll(function(o){return o._markDefs&&o._markDefs()}),Promise.all(this._invokeAll(function(o){return o.beforeRoot&&o.beforeRoot()})).then(function(){return Promise.all([i.getDependencies("scene"),i.getDependencies("animation"),i.getDependencies("camera")])}).then(function(o){let a={scene:o[0][s.scene||0],scenes:o[0],animations:o[1],cameras:o[2],asset:s.asset,parser:i,userData:{}};return ro(r,a,s),ws(a,s),Promise.all(i._invokeAll(function(c){return c.afterRoot&&c.afterRoot(a)})).then(function(){for(let c of a.scenes)c.updateMatrixWorld();e(a)})}).catch(t)}_markDefs(){let e=this.json.nodes||[],t=this.json.skins||[],i=this.json.meshes||[];for(let s=0,r=t.length;s<r;s++){let o=t[s].joints;for(let a=0,c=o.length;a<c;a++)e[o[a]].isBone=!0}for(let s=0,r=e.length;s<r;s++){let o=e[s];o.mesh!==void 0&&(this._addNodeRef(this.meshCache,o.mesh),o.skin!==void 0&&(i[o.mesh].isSkinnedMesh=!0)),o.camera!==void 0&&this._addNodeRef(this.cameraCache,o.camera)}}_addNodeRef(e,t){t!==void 0&&(e.refs[t]===void 0&&(e.refs[t]=e.uses[t]=0),e.refs[t]++)}_getNodeRef(e,t,i){if(e.refs[t]<=1)return i;let s=i.clone(),r=(o,a)=>{let c=this.associations.get(o);c!=null&&this.associations.set(a,c);for(let[l,u]of o.children.entries())r(u,a.children[l])};return r(i,s),s.name+="_instance_"+e.uses[t]++,s}_invokeOne(e){let t=Object.values(this.plugins);t.push(this);for(let i=0;i<t.length;i++){let s=e(t[i]);if(s)return s}return null}_invokeAll(e){let t=Object.values(this.plugins);t.unshift(this);let i=[];for(let s=0;s<t.length;s++){let r=e(t[s]);r&&i.push(r)}return i}getDependency(e,t){let i=e+":"+t,s=this.cache.get(i);if(!s){switch(e){case"scene":s=this.loadScene(t);break;case"node":s=this._invokeOne(function(r){return r.loadNode&&r.loadNode(t)});break;case"mesh":s=this._invokeOne(function(r){return r.loadMesh&&r.loadMesh(t)});break;case"accessor":s=this.loadAccessor(t);break;case"bufferView":s=this._invokeOne(function(r){return r.loadBufferView&&r.loadBufferView(t)});break;case"buffer":s=this.loadBuffer(t);break;case"material":s=this._invokeOne(function(r){return r.loadMaterial&&r.loadMaterial(t)});break;case"texture":s=this._invokeOne(function(r){return r.loadTexture&&r.loadTexture(t)});break;case"skin":s=this.loadSkin(t);break;case"animation":s=this._invokeOne(function(r){return r.loadAnimation&&r.loadAnimation(t)});break;case"camera":s=this.loadCamera(t);break;default:if(s=this._invokeOne(function(r){return r!=this&&r.getDependency&&r.getDependency(e,t)}),!s)throw new Error("Unknown type: "+e);break}this.cache.add(i,s)}return s}getDependencies(e){let t=this.cache.get(e);if(!t){let i=this,s=this.json[e+(e==="mesh"?"es":"s")]||[];t=Promise.all(s.map(function(r,o){return i.getDependency(e,o)})),this.cache.add(e,t)}return t}loadBuffer(e){let t=this.json.buffers[e],i=this.fileLoader;if(t.type&&t.type!=="arraybuffer")throw new Error("THREE.GLTFLoader: "+t.type+" buffer type is not supported.");if(t.uri===void 0&&e===0)return Promise.resolve(this.extensions[Lt.KHR_BINARY_GLTF].body);let s=this.options;return new Promise(function(r,o){i.load(Ys.resolveURL(t.uri,s.path),r,void 0,function(){o(new Error('THREE.GLTFLoader: Failed to load buffer "'+t.uri+'".'))})})}loadBufferView(e){let t=this.json.bufferViews[e];return this.getDependency("buffer",t.buffer).then(function(i){let s=t.byteLength||0,r=t.byteOffset||0;return i.slice(r,r+s)})}loadAccessor(e){let t=this,i=this.json,s=this.json.accessors[e];if(s.bufferView===void 0&&s.sparse===void 0){let o=vf[s.type],a=_a[s.componentType],c=s.normalized===!0,l=new a(s.count*o);return Promise.resolve(new Cn(l,o,c))}let r=[];return s.bufferView!==void 0?r.push(this.getDependency("bufferView",s.bufferView)):r.push(null),s.sparse!==void 0&&(r.push(this.getDependency("bufferView",s.sparse.indices.bufferView)),r.push(this.getDependency("bufferView",s.sparse.values.bufferView))),Promise.all(r).then(function(o){let a=o[0],c=vf[s.type],l=_a[s.componentType],u=l.BYTES_PER_ELEMENT,d=u*c,f=s.byteOffset||0,p=s.bufferView!==void 0?i.bufferViews[s.bufferView].byteStride:void 0,x=s.normalized===!0,b,g;if(p&&p!==d){let m=Math.floor(f/p),A="InterleavedBuffer:"+s.bufferView+":"+s.componentType+":"+m+":"+s.count,U=t.cache.get(A);U||(b=new l(a,m*p,s.count*p/u),U=new Xr(b,p/u),t.cache.add(A,U)),g=new cr(U,c,f%p/u,x)}else a===null?b=new l(s.count*c):b=new l(a,f,s.count*c),g=new Cn(b,c,x);if(s.sparse!==void 0){let m=vf.SCALAR,A=_a[s.sparse.indices.componentType],U=s.sparse.indices.byteOffset||0,T=s.sparse.values.byteOffset||0,I=new A(o[1],U,s.sparse.count*m),L=new l(o[2],T,s.sparse.count*c);a!==null&&(g=new Cn(g.array.slice(),g.itemSize,g.normalized)),g.normalized=!1;for(let P=0,M=I.length;P<M;P++){let C=I[P];if(g.setX(C,L[P*c]),c>=2&&g.setY(C,L[P*c+1]),c>=3&&g.setZ(C,L[P*c+2]),c>=4&&g.setW(C,L[P*c+3]),c>=5)throw new Error("THREE.GLTFLoader: Unsupported itemSize in sparse BufferAttribute.")}g.normalized=x}return g})}loadTexture(e){let t=this.json,i=this.options,r=t.textures[e].source,o=t.images[r],a=this.textureLoader;if(o.uri){let c=i.manager.getHandler(o.uri);c!==null&&(a=c)}return this.loadTextureImage(e,r,a)}loadTextureImage(e,t,i){let s=this,r=this.json,o=r.textures[e],a=r.images[t],c=(a.uri||a.bufferView)+":"+o.sampler;if(this.textureCache[c])return this.textureCache[c];let l=this.loadImageSource(t,i).then(function(u){u.flipY=!1,u.name=o.name||a.name||"",u.name===""&&typeof a.uri=="string"&&a.uri.startsWith("data:image/")===!1&&(u.name=a.uri);let f=(r.samplers||{})[o.sampler]||{};return u.magFilter=G0[f.magFilter]||yn,u.minFilter=G0[f.minFilter]||is,u.wrapS=W0[f.wrapS]||oi,u.wrapT=W0[f.wrapT]||oi,u.generateMipmaps=!u.isCompressedTexture&&u.minFilter!==vn&&u.minFilter!==yn,s.associations.set(u,{textures:e}),u}).catch(function(){return null});return this.textureCache[c]=l,l}loadImageSource(e,t){let i=this,s=this.json,r=this.options;if(this.sourceCache[e]!==void 0)return this.sourceCache[e].then(d=>d.clone());let o=s.images[e],a=self.URL||self.webkitURL,c=o.uri||"",l=!1;if(o.bufferView!==void 0)c=i.getDependency("bufferView",o.bufferView).then(function(d){l=!0;let f=new Blob([d],{type:o.mimeType});return c=a.createObjectURL(f),c});else if(o.uri===void 0)throw new Error("THREE.GLTFLoader: Image "+e+" is missing URI and bufferView");let u=Promise.resolve(c).then(function(d){return new Promise(function(f,p){let x=f;t.isImageBitmapLoader===!0&&(x=function(b){let g=new In(b);g.needsUpdate=!0,f(g)}),t.load(Ys.resolveURL(d,r.path),x,void 0,p)})}).then(function(d){return l===!0&&a.revokeObjectURL(c),ws(d,o),d.userData.mimeType=o.mimeType||_1(o.uri),d}).catch(function(d){throw console.error("THREE.GLTFLoader: Couldn't load texture",c),d});return this.sourceCache[e]=u,u}assignTexture(e,t,i,s){let r=this;return this.getDependency("texture",i.index).then(function(o){if(!o)return null;if(i.texCoord!==void 0&&i.texCoord>0&&(o=o.clone(),o.channel=i.texCoord),r.extensions[Lt.KHR_TEXTURE_TRANSFORM]){let a=i.extensions!==void 0?i.extensions[Lt.KHR_TEXTURE_TRANSFORM]:void 0;if(a){let c=r.associations.get(o);o=r.extensions[Lt.KHR_TEXTURE_TRANSFORM].extendTexture(o,a),r.associations.set(o,c)}}return s!==void 0&&(o.colorSpace=s),e[t]=o,o})}assignFinalMaterial(e){let t=e.geometry,i=e.material,s=t.attributes.tangent===void 0,r=t.attributes.color!==void 0,o=t.attributes.normal===void 0;if(e.isPoints){let a="PointsMaterial:"+i.uuid,c=this.cache.get(a);c||(c=new ur,ni.prototype.copy.call(c,i),c.color.copy(i.color),c.map=i.map,c.sizeAttenuation=!1,this.cache.add(a,c)),i=c}else if(e.isLine){let a="LineBasicMaterial:"+i.uuid,c=this.cache.get(a);c||(c=new zs,ni.prototype.copy.call(c,i),c.color.copy(i.color),c.map=i.map,this.cache.add(a,c)),i=c}if(s||r||o){let a="ClonedMaterial:"+i.uuid+":";s&&(a+="derivative-tangents:"),r&&(a+="vertex-colors:"),o&&(a+="flat-shading:");let c=this.cache.get(a);c||(c=i.clone(),r&&(c.vertexColors=!0),o&&(c.flatShading=!0),s&&(c.normalScale&&(c.normalScale.y*=-1),c.clearcoatNormalScale&&(c.clearcoatNormalScale.y*=-1)),this.cache.add(a,c),this.associations.set(c,this.associations.get(i))),i=c}e.material=i}getMaterialType(){return ge}loadMaterial(e){let t=this,i=this.json,s=this.extensions,r=i.materials[e],o,a={},c=r.extensions||{},l=[];if(c[Lt.KHR_MATERIALS_UNLIT]){let d=s[Lt.KHR_MATERIALS_UNLIT];o=d.getMaterialType(),l.push(d.extendParams(a,r,t))}else{let d=r.pbrMetallicRoughness||{};if(a.color=new ke(1,1,1),a.opacity=1,Array.isArray(d.baseColorFactor)){let f=d.baseColorFactor;a.color.setRGB(f[0],f[1],f[2],ti),a.opacity=f[3]}d.baseColorTexture!==void 0&&l.push(t.assignTexture(a,"map",d.baseColorTexture,sn)),a.metalness=d.metallicFactor!==void 0?d.metallicFactor:1,a.roughness=d.roughnessFactor!==void 0?d.roughnessFactor:1,d.metallicRoughnessTexture!==void 0&&(l.push(t.assignTexture(a,"metalnessMap",d.metallicRoughnessTexture)),l.push(t.assignTexture(a,"roughnessMap",d.metallicRoughnessTexture))),o=this._invokeOne(function(f){return f.getMaterialType&&f.getMaterialType(e)}),l.push(Promise.all(this._invokeAll(function(f){return f.extendMaterialParams&&f.extendMaterialParams(e,a)})))}r.doubleSided===!0&&(a.side=mn);let u=r.alphaMode||yf.OPAQUE;if(u===yf.BLEND?(a.transparent=!0,a.depthWrite=!1):(a.transparent=!1,u===yf.MASK&&(a.alphaTest=r.alphaCutoff!==void 0?r.alphaCutoff:.5)),r.normalTexture!==void 0&&o!==ln&&(l.push(t.assignTexture(a,"normalMap",r.normalTexture)),a.normalScale=new Pe(1,1),r.normalTexture.scale!==void 0)){let d=r.normalTexture.scale;a.normalScale.set(d,d)}if(r.occlusionTexture!==void 0&&o!==ln&&(l.push(t.assignTexture(a,"aoMap",r.occlusionTexture)),r.occlusionTexture.strength!==void 0&&(a.aoMapIntensity=r.occlusionTexture.strength)),r.emissiveFactor!==void 0&&o!==ln){let d=r.emissiveFactor;a.emissive=new ke().setRGB(d[0],d[1],d[2],ti)}return r.emissiveTexture!==void 0&&o!==ln&&l.push(t.assignTexture(a,"emissiveMap",r.emissiveTexture,sn)),Promise.all(l).then(function(){let d=new o(a);return r.name&&(d.name=r.name),ws(d,r),t.associations.set(d,{materials:e}),r.extensions&&ro(s,d,r),d})}createUniqueName(e){let t=en.sanitizeNodeName(e||"");return t in this.nodeNamesUsed?t+"_"+ ++this.nodeNamesUsed[t]:(this.nodeNamesUsed[t]=0,t)}loadGeometries(e){let t=this,i=this.extensions,s=this.primitiveCache;function r(a){return i[Lt.KHR_DRACO_MESH_COMPRESSION].decodePrimitive(a,t).then(function(c){return X0(c,a,t)})}let o=[];for(let a=0,c=e.length;a<c;a++){let l=e[a],u=g1(l),d=s[u];if(d)o.push(d.promise);else{let f;l.extensions&&l.extensions[Lt.KHR_DRACO_MESH_COMPRESSION]?f=r(l):f=X0(new tn,l,t),l.mode===Oi.TRIANGLE_STRIP?f=f.then(p=>xf(p,Cl)):l.mode===Oi.TRIANGLE_FAN&&(f=f.then(p=>xf(p,ha))),s[u]={primitive:l,promise:f},o.push(f)}}return Promise.all(o)}loadMesh(e){let t=this,i=this.json,s=this.extensions,r=i.meshes[e],o=r.primitives,a=[];for(let c=0,l=o.length;c<l;c++){let u=o[c].material===void 0?f1(this.cache):this.getDependency("material",o[c].material);a.push(u)}return a.push(t.loadGeometries(o)),Promise.all(a).then(async function(c){let l=c.slice(0,c.length-1),u=c[c.length-1],d=[];for(let p=0,x=u.length;p<x;p++){let b=u[p],g=o[p],m,A=l[p];if(g.mode===Oi.TRIANGLES||g.mode===Oi.TRIANGLE_STRIP||g.mode===Oi.TRIANGLE_FAN||g.mode===void 0){let U=r.isSkinnedMesh===!0,T=b.hasAttribute("skinIndex")&&b.hasAttribute("skinWeight");U&&T===!1&&console.warn("THREE.GLTFLoader: Missing skinIndex or skinWeight attributes. Skinning disabled."),m=U&&T?new tl(b,A):new dn(b,A),m.isSkinnedMesh===!0&&m.normalizeSkinWeights()}else if(g.mode===Oi.LINES)m=new hr(b,A);else if(g.mode===Oi.LINE_STRIP)m=new qr(b,A);else if(g.mode===Oi.LINE_LOOP)m=new il(b,A);else if(g.mode===Oi.POINTS)m=new Yr(b,A);else throw new Error("THREE.GLTFLoader: Primitive mode unsupported: "+g.mode);Object.keys(m.geometry.morphAttributes).length>0&&m1(m,r),m.name=t.createUniqueName(r.name||"mesh_"+e),ws(m,r),g.extensions&&ro(s,m,g),t.assignFinalMaterial(m),d.push(m)}for(let p=0,x=d.length;p<x;p++)t.associations.set(d[p],{meshes:e,primitives:p});if(d.length===1)return r.extensions&&ro(s,d[0],r),d[0];let f=new Oe;r.extensions&&ro(s,f,r),t.associations.set(f,{meshes:e});for(let p=0,x=d.length;p<x;p++)f.add(d[p]);return f})}loadCamera(e){let t,i=this.json.cameras[e],s=i[i.type];if(!s){console.warn("THREE.GLTFLoader: Missing camera parameters.");return}return i.type==="perspective"?t=new An(Zs.radToDeg(s.yfov),s.aspectRatio||1,s.znear||1,s.zfar||2e6):i.type==="orthographic"&&(t=new mr(-s.xmag,s.xmag,s.ymag,-s.ymag,s.znear,s.zfar)),i.name&&(t.name=this.createUniqueName(i.name)),ws(t,i),Promise.resolve(t)}loadSkin(e){let t=this.json.skins[e],i=[];for(let s=0,r=t.joints.length;s<r;s++)i.push(this._loadNodeShallow(t.joints[s]));return t.inverseBindMatrices!==void 0?i.push(this.getDependency("accessor",t.inverseBindMatrices)):i.push(null),Promise.all(i).then(function(s){let r=s.pop(),o=s,a=[],c=[];for(let l=0,u=o.length;l<u;l++){let d=o[l];if(d){a.push(d);let f=new rt;r!==null&&f.fromArray(r.array,l*16),c.push(f)}else console.warn('THREE.GLTFLoader: Joint "%s" could not be found.',t.joints[l])}return new nl(a,c)})}loadAnimation(e){let t=this.json,i=this,s=t.animations[e],r=s.name?s.name:"animation_"+e,o=[],a=[],c=[],l=[],u=[];for(let d=0,f=s.channels.length;d<f;d++){let p=s.channels[d],x=s.samplers[p.sampler],b=p.target,g=b.node,m=s.parameters!==void 0?s.parameters[x.input]:x.input,A=s.parameters!==void 0?s.parameters[x.output]:x.output;b.node!==void 0&&(o.push(this.getDependency("node",g)),a.push(this.getDependency("accessor",m)),c.push(this.getDependency("accessor",A)),l.push(x),u.push(b))}return Promise.all([Promise.all(o),Promise.all(a),Promise.all(c),Promise.all(l),Promise.all(u)]).then(function(d){let f=d[0],p=d[1],x=d[2],b=d[3],g=d[4],m=[];for(let U=0,T=f.length;U<T;U++){let I=f[U],L=p[U],P=x[U],M=b[U],C=g[U];if(I===void 0)continue;I.updateMatrix&&I.updateMatrix();let O=i._createAnimationTracks(I,L,P,M,C);if(O)for(let H=0;H<O.length;H++)m.push(O[H])}let A=new ul(r,void 0,m);return ws(A,s),A})}createNodeMesh(e){let t=this.json,i=this,s=t.nodes[e];return s.mesh===void 0?null:i.getDependency("mesh",s.mesh).then(function(r){let o=i._getNodeRef(i.meshCache,s.mesh,r);return s.weights!==void 0&&o.traverse(function(a){if(a.isMesh)for(let c=0,l=s.weights.length;c<l;c++)a.morphTargetInfluences[c]=s.weights[c]}),o})}loadNode(e){let t=this.json,i=this,s=t.nodes[e],r=i._loadNodeShallow(e),o=[],a=s.children||[];for(let l=0,u=a.length;l<u;l++)o.push(i.getDependency("node",a[l]));let c=s.skin===void 0?Promise.resolve(null):i.getDependency("skin",s.skin);return Promise.all([r,Promise.all(o),c]).then(function(l){let u=l[0],d=l[1],f=l[2];f!==null&&u.traverse(function(p){p.isSkinnedMesh&&p.bind(f,x1)});for(let p=0,x=d.length;p<x;p++)u.add(d[p]);if(u.userData.pivot!==void 0&&d.length>0){let p=u.userData.pivot,x=d[0];u.pivot=new y().fromArray(p),u.position.x-=p[0],u.position.y-=p[1],u.position.z-=p[2],x.position.set(0,0,0),delete u.userData.pivot}return u})}_loadNodeShallow(e){let t=this.json,i=this.extensions,s=this;if(this.nodeCache[e]!==void 0)return this.nodeCache[e];let r=t.nodes[e],o=r.name?s.createUniqueName(r.name):"",a=[],c=s._invokeOne(function(l){return l.createNodeMesh&&l.createNodeMesh(e)});return c&&a.push(c),r.camera!==void 0&&a.push(s.getDependency("camera",r.camera).then(function(l){return s._getNodeRef(s.cameraCache,r.camera,l)})),s._invokeAll(function(l){return l.createNodeAttachment&&l.createNodeAttachment(e)}).forEach(function(l){a.push(l)}),this.nodeCache[e]=Promise.all(a).then(function(l){let u;if(r.isBone===!0?u=new Jo:l.length>1?u=new Oe:l.length===1?u=l[0]:u=new an,u!==l[0])for(let d=0,f=l.length;d<f;d++)u.add(l[d]);if(r.name&&(u.userData.name=r.name,u.name=o),ws(u,r),r.extensions&&ro(i,u,r),r.matrix!==void 0){let d=new rt;d.fromArray(r.matrix),u.applyMatrix4(d)}else r.translation!==void 0&&u.position.fromArray(r.translation),r.rotation!==void 0&&u.quaternion.fromArray(r.rotation),r.scale!==void 0&&u.scale.fromArray(r.scale);if(!s.associations.has(u))s.associations.set(u,{});else if(r.mesh!==void 0&&s.meshCache.refs[r.mesh]>1){let d=s.associations.get(u);s.associations.set(u,{...d})}return s.associations.get(u).nodes=e,u}),this.nodeCache[e]}loadScene(e){let t=this.extensions,i=this.json.scenes[e],s=this,r=new Oe;i.name&&(r.name=s.createUniqueName(i.name)),ws(r,i),i.extensions&&ro(t,r,i);let o=i.nodes||[],a=[];for(let c=0,l=o.length;c<l;c++)a.push(s.getDependency("node",o[c]));return Promise.all(a).then(function(c){for(let u=0,d=c.length;u<d;u++){let f=c[u];f.parent!==null?r.add(k0(f)):r.add(f)}let l=u=>{let d=new Map;for(let[f,p]of s.associations)(f instanceof ni||f instanceof In)&&d.set(f,p);return u.traverse(f=>{let p=s.associations.get(f);p!=null&&d.set(f,p)}),d};return s.associations=l(r),r})}_createAnimationTracks(e,t,i,s,r){let o=[],a=e.name?e.name:e.uuid,c=[];function l(p){p.morphTargetInfluences&&c.push(p.name?p.name:p.uuid)}vr[r.path]===vr.weights?(l(e),e.isGroup&&e.children.forEach(l)):c.push(a);let u;switch(vr[r.path]){case vr.weights:u=Ws;break;case vr.rotation:u=Xs;break;case vr.translation:case vr.scale:u=pr;break;default:i.itemSize===1?u=Ws:u=pr;break}let d=s.interpolation!==void 0?d1[s.interpolation]:zr,f=this._getArrayFromAccessor(i);for(let p=0,x=c.length;p<x;p++){let b=new u(c[p]+"."+vr[r.path],t.array,f,d);s.interpolation==="CUBICSPLINE"&&this._createCubicSplineTrackInterpolant(b),o.push(b)}return o}_getArrayFromAccessor(e){let t=e.array;if(e.normalized){let i=Xf(t.constructor),s=new Float32Array(t.length);for(let r=0,o=t.length;r<o;r++)s[r]=t[r]*i;t=s}return t}_createCubicSplineTrackInterpolant(e){e.createInterpolant=function(i){let s=this instanceof Xs?Gf:xu;return new s(this.times,this.values,this.getValueSize()/3,i)},e.createInterpolant.isInterpolantFactoryMethodGLTFCubicSpline=!0}};function v1(n,e,t){let i=e.attributes,s=new un;if(i.POSITION!==void 0){let a=t.json.accessors[i.POSITION],c=a.min,l=a.max;if(c!==void 0&&l!==void 0){if(s.set(new y(c[0],c[1],c[2]),new y(l[0],l[1],l[2])),a.normalized){let u=Xf(_a[a.componentType]);s.min.multiplyScalar(u),s.max.multiplyScalar(u)}}else{console.warn("THREE.GLTFLoader: Missing min/max properties for accessor POSITION.");return}}else return;let r=e.targets;if(r!==void 0){let a=new y,c=new y;for(let l=0,u=r.length;l<u;l++){let d=r[l];if(d.POSITION!==void 0){let f=t.json.accessors[d.POSITION],p=f.min,x=f.max;if(p!==void 0&&x!==void 0){if(c.setX(Math.max(Math.abs(p[0]),Math.abs(x[0]))),c.setY(Math.max(Math.abs(p[1]),Math.abs(x[1]))),c.setZ(Math.max(Math.abs(p[2]),Math.abs(x[2]))),f.normalized){let b=Xf(_a[f.componentType]);c.multiplyScalar(b)}a.max(c)}else console.warn("THREE.GLTFLoader: Missing min/max properties for accessor POSITION.")}}s.expandByVector(a)}n.boundingBox=s;let o=new li;s.getCenter(o.center),o.radius=s.min.distanceTo(s.max)/2,n.boundingSphere=o}function X0(n,e,t){let i=e.attributes,s=[];function r(o,a){return t.getDependency("accessor",o).then(function(c){n.setAttribute(a,c)})}for(let o in i){let a=Wf[o]||o.toLowerCase();a in n.attributes||s.push(r(i[o],a))}if(e.indices!==void 0&&!n.index){let o=t.getDependency("accessor",e.indices).then(function(a){n.setIndex(a)});s.push(o)}return It.workingColorSpace!==ti&&"COLOR_0"in i&&console.warn(`THREE.GLTFLoader: Converting vertex colors from "srgb-linear" to "${It.workingColorSpace}" not supported.`),ws(n,e),v1(n,e,t),Promise.all(s).then(function(){return e.targets!==void 0?p1(n,e.targets,t):n})}function Y0(n){var e=0;function t(xe,vt,Rt,X,xn){var lt=n.mesh(xe,vt,Rt,X,xn);return e++,lt}var i=new ge({color:"#737b7e",roughness:.85,metalness:.08}),s=new ge({color:"#8b9396",roughness:.48,metalness:.7}),r=new ge({color:"#cbd4d6",roughness:.2,metalness:.05}),o=[i,s,r];for(var a in n.EQ){var c=n.EQ[a],l=c.g,u=c.e,d=n.mm(u.L),f=n.mm(u.H),p=n.mm(u.W);if(u.type==="chiller"){for(var x of[-1,1])for(var b of[{h:1.08,z:.18,r:.44},{h:.62,z:-.22,r:.38}]){t(n.cyl(b.r*.96,.018,40),i,l,new y(x*d*.474,b.h,b.z),[0,0,Math.PI/2]);for(var g=0;g<12;g++){var m=g*Math.PI/6;t(n.cyl(.018,.035,6),s,l,new y(x*d*.482,b.h+Math.sin(m)*b.r*.88,b.z+Math.cos(m)*b.r*.88),[0,0,Math.PI/2])}}for(var A of[-.25,0,.25])t(new bi(.425,.006,6,40),i,l,new y(d*A,1.08,.18),[0,Math.PI/2,0]),t(new bi(.365,.006,6,40),i,l,new y(d*A,.62,-.22),[0,Math.PI/2,0]);t(n.box(.16,.05,.012),i,l,new y(d*.5+.189,1.05,.55),[0,Math.PI/2,0]);var U=n.textSprite(u.id,27,"#35474f",null);U.position.set(d*.5+.196,1.12,.1),U.scale.set(.32,.16,1),U.rotation.y=Math.PI/2,l.add(U)}else if(u.type==="pump"){t(n.box(.22,.12,.16,.01),n.MAT.motor,l,new y(d*.22,.86,0));for(var T of[-1,1])for(var I of[-1,1])t(n.cyl(.018,.02,6),s,l,new y(T*d*.42,.375,I*p*.3));t(n.cyl(.008,.2,8),n.MAT.galv,l,new y(-d*.3,1.18,0)),t(n.cyl(.045,.025,20),n.MAT.galv,l,new y(-d*.3,1.29,0),[Math.PI/2,0,0]),t(n.cyl(.038,.028,20),r,l,new y(-d*.3,1.29,.016),[Math.PI/2,0,0]),t(n.box(.005,.042,.004),i,l,new y(-d*.3,1.3,.034),[0,0,-.5])}else if(u.type==="ct"){for(var L=-d*.4;L<d*.5;L+=.52)for(var P of[-p/2-.044,p/2+.044]){t(n.box(.016,f-.66,.012),i,l,new y(L,f/2+.28,P));for(var M of[.7,f-.18])t(n.cyl(.012,.008,6),s,l,new y(L,M,P),[Math.PI/2,0,0])}for(var C=0;C<10;C++)t(n.box(d,.016,.02),n.MAT.galv,l,new y(0,f+.024,p/2+.12+C*.035))}else if(u.type==="ahu")for(var O of[-.32,.05,.35])t(n.box(.012,f*.88,.014),i,l,new y(d*O,f/2,p/2+.032)),t(n.box(.012,.16,.04),n.MAT.black,l,new y(d*O+.08,f*.5,p/2+.05));o.forEach(function(xe){c.mats.add(xe.clone())})}for(var H=new ge({color:"#d6d3ca",roughness:.85,metalness:.03}),k=new ge({color:"#68767e",roughness:.65,metalness:.5}),q=1;q<=n.BLD.floors;q++){var z=new Oe;n.LAYER.shell.add(z),n.onFloor(q,z);var ee=n.zOf(q),he=(q===1?n.BLD.f1_h:n.BLD.typ_h)-n.BLD.slab;for(var ue of[0,n.BLD.y]){t(n.box(n.mm(n.BLD.x),.34,.08),H,z,n.P3(n.BLD.x/2,ue,ee+260)),t(n.box(n.mm(n.BLD.x),.055,.08),k,z,n.P3(n.BLD.x/2,ue,ee+he*.58));for(var ye=2e3;ye<n.BLD.x;ye+=8e3)t(n.box(.12,n.mm(he),.32),H,z,n.P3(ye,ue,ee+he/2))}for(var V of[0,n.BLD.x])t(n.box(.08,.34,n.mm(n.BLD.y)),H,z,n.P3(V,n.BLD.y/2,ee+260)),t(n.box(.08,.055,n.mm(n.BLD.y)),k,z,n.P3(V,n.BLD.y/2,ee+he*.58))}var Q=new Oe;n.LAYER.shell.add(Q),n.onFloor(9,Q);for(var le=4e3;le<n.BLD.x;le+=4e3)t(n.box(.018,.006,n.mm(n.BLD.y)),i,Q,n.P3(le,n.BLD.y/2,n.ROOFZ+4));for(var Ee=4e3;Ee<n.BLD.y;Ee+=4e3)t(n.box(n.mm(n.BLD.x),.006,.018),i,Q,n.P3(n.BLD.x/2,Ee,n.ROOFZ+4));for(var be of[[n.BLD.x/2,0,n.BLD.x,380],[n.BLD.x/2,n.BLD.y,n.BLD.x,380],[0,n.BLD.y/2,380,n.BLD.y],[n.BLD.x,n.BLD.y/2,380,n.BLD.y]])t(n.box(n.mm(be[2]),.045,n.mm(be[3])),n.MAT.galv,Q,n.P3(be[0],be[1],n.ROOFZ+n.BLD.parapet+20));var ut=new Oe;n.LAYER.shell.add(ut),n.onFloor(1,ut),t(n.box(10,.18,3.2),H,ut,n.P3(54e3,-1400,3600));for(var et of[5e4,58e3])t(n.box(.18,3.55,.18),k,ut,n.P3(et,-2500,1775));t(n.box(11,.1,4.2),n.MAT.concrete,ut,n.P3(54e3,-1800,-50));var ct=document.createElement("div");ct.className="material-note",ct.textContent="Reference geometry \xB7 reference material colours, not as-built",document.querySelector("aside section").appendChild(ct);var ae=Array.from(document.querySelector("aside section").querySelectorAll("h2")).find(function(xe){return xe.textContent.includes("Future systems")});if(ae){var me=document.createElement("details"),qe=document.createElement("summary");qe.textContent="Future systems",ae.replaceWith(me),me.appendChild(qe),me.appendChild(n.$("sysl"))}var ft=n.$("sim").querySelector("h2");if(ft){var Ge=document.createElement("details"),Et=document.createElement("summary");for(Et.textContent="Alarm simulation (DEMO)",ft.remove(),Ge.appendChild(Et);n.$("sim").firstChild;)Ge.appendChild(n.$("sim").firstChild);n.$("sim").appendChild(Ge)}var pn=document.querySelector(".zrow"),bt=document.querySelector('[data-layer="zones"]');pn&&bt&&(pn.style.display="none",bt.addEventListener("change",function(){pn.style.display=bt.checked?"":"none"}));for(var Ft of["zones","systems"]){var Wt=document.querySelector('[data-layer="'+Ft+'"]');Wt&&(Wt.checked=!1,n.LAYER[Ft].visible=!1)}var Tt=document.createElement("label");Tt.style.display="block",Tt.style.marginTop="7px",Tt.innerHTML='<input type="checkbox" id="showSpare"> Show empty (not installed) slots',document.querySelector("aside section").appendChild(Tt);function Jt(){var xe=n.$("showSpare").checked;for(var vt in n.EQ)n.EQ[vt].ghost&&(n.EQ[vt].g.visible=xe&&(!n.ISO||n.FSEL==="all"||n.FSEL==="roof"||n.EQ[vt].e.floor==+n.FSEL||!n.EQ[vt].e.floor&&n.FSEL==="1"));for(var vt in n.PIPE)n.PIPE[vt].ghost&&(n.PIPE[vt].g.visible=xe)}var bn=n.updateGhosts;n.updateGhosts=function(){bn(),Jt()},n.$("showSpare").onchange=function(){n.applyFloor(),Jt()},document.querySelectorAll("[data-view]").forEach(function(xe){xe.addEventListener("click",function(){document.querySelectorAll("[data-view]").forEach(function(Rt){Rt.classList.toggle("active",Rt===xe)});var vt=document.querySelector('[data-layer="shell"]');vt.checked=!["plant","pumps","room","floor"].includes(xe.dataset.view),n.LAYER.shell.visible=vt.checked,n.$("info").className=""})}),window.__DESIGN={version:"2026-10-10",detailMeshCount:e,inspect:function(){return{equipment:Object.keys(n.EQ).length,pipes:Object.keys(n.PIPE).length,detailMeshCount:e,mode:n.DEMO?"DEMO":document.getElementById("mode").textContent,camera:n.camera.position.toArray(),materials:{chiller:n.MAT.almond.color.getHexString(),pump:n.MAT.motor.color.getHexString(),tower:n.MAT.frp.color.getHexString()},renderer:n.renderer.info.render,triangles:n.renderer.info.render.triangles}}},(function(){var xe=window.OFFICE_DESIGN,vt=xe.rooms,Rt={},X=[],xn=[],lt={concrete:new ge({color:"#9f9d94",map:n.T.concrete,roughness:.92}),wall:new ge({color:"#d0c9b9",roughness:.93}),frame:new ge({color:"#263b45",roughness:.45,metalness:.65}),metal:new ge({color:"#89999e",roughness:.38,metalness:.75}),carpet:new ge({color:"#6b7473",roughness:1}),tile:new ge({color:"#a39c8b",roughness:.67}),wood:new ge({color:"#b59872",roughness:.75}),chair:new ge({color:"#273c46",roughness:.86}),sofa:new ge({color:"#697068",roughness:.96}),screen:new ge({color:"#16262c",emissive:"#18475a",emissiveIntensity:.25}),duct:new ge({color:"#7f9199",metalness:.72,roughness:.38}),returnDuct:new ge({color:"#7b817d",metalness:.65,roughness:.43}),insulated:new ge({color:"#323d40",roughness:.88}),SA:new ge({color:"#47c7f5",roughness:.6}),RA:new ge({color:"#bb9bea",roughness:.65}),OA:new ge({color:"#43d19b",roughness:.62}),KE:new ge({color:"#7d6055",roughness:.7}),MA:new ge({color:"#77999c",roughness:.6}),TE:new ge({color:"#f28d64",roughness:.7}),EA:new ge({color:"#f28d64",roughness:.65}),TA:new ge({color:"#879c94",roughness:.65}),PA:new ge({color:"#6f8f8b",roughness:.65}),PE:new ge({color:"#8b8178",roughness:.65}),glass:new ge({color:"#b0c3c1",transparent:!0,opacity:.18,depthWrite:!1,roughness:.15,metalness:.15,side:mn}),luminaire:new ge({color:"#fff0ce",emissive:"#ffe1ad",emissiveIntensity:2.2,roughness:.6}),foliage:new ge({color:"#334e3d",roughness:1}),pot:new ge({color:"#786b59",roughness:.9}),blue:new ge({color:"#315e7b",metalness:.45,roughness:.45})};for(var B in lt)lt[B].envMapIntensity=.035;lt.wood.map=n.canvasTex(256,256,function(h,_,v){h.fillStyle="#b49b80",h.fillRect(0,0,_,v);for(var S=0;S<100;S++)h.strokeStyle=S%3?"rgba(64,42,23,.10)":"rgba(235,221,199,.16)",h.beginPath(),h.moveTo(0,S*3),h.bezierCurveTo(80,S*3+2,170,S*3-2,256,S*3+1),h.stroke()},[2,2]),lt.carpet.map=n.canvasTex(128,128,function(h,_,v){h.fillStyle="#bbbbbb",h.fillRect(0,0,_,v);for(var S=0;S<v;S+=2)for(var w=0;w<_;w+=2)h.fillStyle=(w+S)%4?"#999999":"#cccccc",h.fillRect(w,S,1,1)},[16,16]);var E=function(h){return h===0?6:h===1?5.5:4.2},$=function(h){return h===0?-6:h===1?0:h===9?34.9:5.5+(h-2)*4.2};function se(h,_,v){return[0,1,2].every(function(S){return h[S]<_[S+3]+(v||0)&&h[S+3]>_[S]-(v||0)})}function de(h,_,v,S,w,F,N){var D=Math.abs(Math.cos(N||0)),Y=Math.abs(Math.sin(N||0)),J=S*D+F*Y,K=S*Y+F*D;return[h-J/2,v-K/2,_-w/2,h+J/2,v+K/2,_+w/2]}function we(h){return xe.columns.filter(function(_){return _.floor===h})}function Ae(h,_,v,S){var w={},F=S?0:$(_);return{box:function(N,D,Y,J,K,fe,te,pe,ze){if(!(K<.001||fe<.001||te<.001)){var Ue=de(D,Y+F,J,K,fe,te,pe);if(ze&&we(_).some(function(at){return se(Ue,at.box,.025)})){xn.push({floor:_,kind:v,material:N,box:Ue});return}(w[N]||(w[N]=[])).push([D,Y,-J,K,fe,te,pe||0]),v!=="structure"&&v!=="envelope"&&X.push({floor:_,kind:v==="furniture"&&fe<=.04&&Y<.1?"finish":v,material:N,box:Ue})}},flush:function(){var N=new _t(1,1,1),D=N.attributes.position,Y=N.attributes.normal,J=N.attributes.uv,K=N.index;for(var fe in w){var te=[],pe=[],ze=[],Ue=[];w[fe].forEach(function(dt){for(var Rn=Math.cos(dt[6]),Xi=Math.sin(dt[6]),ps=te.length/3,Ht=0;Ht<D.count;Ht++){var qi=D.getX(Ht)*dt[3],Ds=D.getZ(Ht)*dt[5];te.push(dt[0]+qi*Rn+Ds*Xi,dt[1]+D.getY(Ht)*dt[4],dt[2]-qi*Xi+Ds*Rn),qi=Y.getX(Ht),Ds=Y.getZ(Ht),pe.push(qi*Rn+Ds*Xi,Y.getY(Ht),-qi*Xi+Ds*Rn),ze.push(J.getX(Ht),J.getY(Ht))}for(var Ht=0;Ht<K.count;Ht++)Ue.push(ps+K.getX(Ht))});var at=new _t(1,1,1);at.setAttribute("position",new D.constructor(te,3)),at.setAttribute("normal",new Y.constructor(pe,3)),at.setAttribute("uv",new J.constructor(ze,2)),at.setIndex(Ue),at.clearGroups(),at.computeBoundingSphere();var on=n.mesh(at,lt[fe].clone(),h);on.userData.designKind=v}N.dispose()}}}function ce(h,_,v,S,w,F){var N=document.createElement("canvas");N.width=512,N.height=96;var D=N.getContext("2d");D.textAlign="center",D.fillStyle="#e9e0cd",D.font="600 34px Segoe UI",D.fillText(_,256,62);var Y=new ci(N);Y.colorSpace=sn;var J=n.mesh(new cn(F,F*.1875),new ln({map:Y,transparent:!0,depthWrite:!1}),h,new y(v,S,-w),[-Math.PI/2,0,0]);return J}function re(h,_,v,S,w,F,N,D){var Y=Math.hypot(w-v,F-S),J=(w-v)/Y,K=(F-S)/Y,fe=Math.atan2(F-S,w-v),te=[];we(_).forEach(function(dt){var Rn=(dt.box[0]+dt.box[3])/2,Xi=(dt.box[1]+dt.box[4])/2,ps=(Rn-v)*J+(Xi-S)*K,Ht=Math.abs((Rn-v)*K-(Xi-S)*J);Ht<.39&&ps>-.4&&ps<Y+.4&&te.push([Math.max(0,ps-.4),Math.min(Y,ps+.4)])}),N!==void 0&&te.push([Math.max(.2,N),Math.min(Y-.2,N+1.1)]),te.sort(function(dt,Rn){return dt[0]-Rn[0]});var pe=[],ze=0;te.forEach(function(dt){dt[0]>ze&&pe.push([ze,dt[0]]),ze=Math.max(ze,dt[1])}),ze<Y&&pe.push([ze,Y]);function Ue(dt,Rn,Xi,ps,Ht,qi){Rn-dt<.02||h.box(Ht,v+J*(dt+Rn)/2,Xi,S+K*(dt+Rn)/2,Rn-dt,ps,qi||.12,fe,!0)}if(pe.forEach(function(dt){D?(Ue(dt[0],dt[1],.22,.44,"wall"),Ue(dt[0],dt[1],1.65,2.36,"glass",.025),Ue(dt[0],dt[1],2.85,.055,"frame",.065),Ue(dt[0],dt[0]+.04,1.62,2.55,"frame",.07),Ue(dt[1]-.04,dt[1],1.62,2.55,"frame",.07)):Ue(dt[0],dt[1],1.45,2.9,"wall"),Ue(dt[0],dt[1],.06,.12,"frame",.13)}),N!==void 0){var at=Math.max(.2,N),on=Math.min(Y-.2,N+1.1);Ue(at,on,2.65,.5,"wall"),Ue(at+.03,on-.03,1.08,2.14,D?"glass":"wood",.045),Ue(at,at+.04,1.13,2.26,"frame",.08),Ue(on-.04,on,1.13,2.26,"frame",.08),Ue(at,on,2.25,.045,"frame",.08),Ue(on-.16,on-.1,1.05,.035,"metal",.13)}}function Ie(h,_,v,S){var w=S?2.8:1.4,F=S?1.1:.7;h.box("wood",_,.74,v,w,.065,F,0,!0);for(var N of[-w*.38,w*.38])h.box("frame",_+N,.36,v,.05,.7,F*.7,0,!0);if(!S)h.box("screen",_,.98,v-.05,.45,.29,.035,0,!0),h.box("frame",_,.83,v-.05,.12,.14,.08,0,!0),h.box("chair",_,.43,v+.7,.45,.08,.43,0,!0),h.box("chair",_,.68,v+.85,.45,.5,.06,0,!0);else for(var D of[-1,1])for(var N of[-.85,.85])h.box("chair",_+N,.44,v+D*.9,.48,.08,.43,0,!0),h.box("chair",_+N,.7,v+D*1.07,.48,.48,.06,0,!0)}function Ze(h,_,v){h.box("pot",_,.22,v,.4,.44,.4,0,!0),h.box("foliage",_,.72,v,.66,.7,.6,0,!0)}function Fe(h,_,v,S,w){for(var F=0;F<S;F++)oe(h,_+(F-(S-1)/2)*1.5,v,w)}function Se(h,_,v,S){h.box("wood",_,.52,v,S,1,.42,0,!0),h.box("frame",_,.72,v+.22,S-.06,.025,.035,0,!0)}function it(h,_){var v=_.rect,S=v[0],w=v[1],F=v[2],N=v[3],D=(S+F)/2,Y=(w+N)/2,J=_.layoutVariant;if(_.id==="G-REC"){h.box("wood",D,.95,w+1.3,4.6,.12,.85,0,!0),h.box("wall",D,.46,w+1.3,4.4,.85,.75,0,!0),oe(h,S+2,N-2.2,0),oe(h,F-2,N-2.2,0),Re(h,D,w+3.3,2.4,0);return}var K=S<40&&_.floor>1,fe=Y<18?N-_.privateDepth_m:w+_.privateDepth_m,te=K?Y<18?w:fe+.12:w,pe=K&&Y<18?fe-.12:N,ze=(te+pe)/2;if(J===0){for(var Ue of[te+2.1,pe-2.4])oe(h,D-.9,Ue,0),oe(h,D+.9,Ue,0);Se(h,S+.6,ze,1)}if(J===1&&(oe(h,D,te+(_.id.endsWith("EN2")?3.3:2),Math.PI),Re(h,D,pe-1.6,2.7,0),h.box("wood",D,.38,pe-2.8,1.25,.06,.65,0,!0),Se(h,D,te+.5,2.5)),J===2&&(oe(h,S+1.1,te+2.1,Math.PI/2),oe(h,F-1.1,pe-2.2,-Math.PI/2),h.box("wood",D,.87,ze,2.5,.08,1.2,0,!0),h.box("wall",F-.25,1.55,ze,.05,1,2.2,0,!0)),J===3&&(oe(h,S+1.4,te+1.6,0),oe(h,F-1.4,pe-2,Math.PI),Ie(h,D,ze,!0),Se(h,S+.5,ze,.75)),J===4){for(var Ue=te+1.7;Ue<pe-1.8;Ue+=2.5)oe(h,D-.95,Ue,Math.PI),oe(h,D+.95,Ue,Math.PI);h.box("screen",D,1.8,te+.2,1.9,1.1,.06,0,!0)}if(J===5&&(oe(h,D,te+1.9,0),oe(h,D,pe-2,Math.PI),Re(h,S+.7,ze,2.1,Math.PI/2),h.box("wood",F-.75,.8,ze,.9,.07,2.1,0,!0)),K){var at=Y<18?(fe+N)/2:(w+fe)/2;J===1?oe(h,D,at,0):J===5?(oe(h,D,at,Math.PI/2),Se(h,F-.4,at,.6)):Ie(h,D,at,!0)}Ze(h,F-.65,te+.65)}function ot(h,_){var v=_.rect,S=(v[0]+v[2])/2,w=(v[1]+v[3])/2,F=_.layoutVariant;if(F===0&&Ie(h,S,w,!0),F===1)for(var N of[S-1.45,S+1.45])for(var D of[w-.85,w+.85])oe(h,N,D,Math.PI);if(F===2){h.box("wood",S,.74,w,2.2,.065,.9,0,!0);for(var N of[S-.7,S+.7])Te(h,N,w+.9,0);h.box("screen",S,1.65,v[1]+.16,1.8,1.05,.06,0,!0)}if(F===3){h.box("wood",S,.9,w,2.2,.065,1.2,0,!0);for(var N of[S-1.35,S+1.35])Te(h,N,w,Math.PI/2);h.box("wall",S,1.7,v[3]-.15,2.5,1.1,.05,0,!0)}F!==2&&h.box("screen",S,1.7,v[1]+.17,1.35,.75,.05,0,!0)}function xt(h,_){var v=_.rect,S=v[0],w=v[1],F=v[2],N=v[3],D=(S+F)/2,Y=(w+N)/2;if(_.r6)return W(h,_);if(_.kind==="office")return it(h,_);if(_.kind==="meeting")return ot(h,_);if(_.kind==="lobby")if(_.id==="G-LOB"){h.box("wood",23,.9,5,5,.12,1.1,0,!0),h.box("wall",23,.43,5,4.8,.8,1,0,!0);for(var J of[6,13,20])Re(h,J,10.5,3.2,0),h.box("wood",J,.37,9.2,1.4,.06,.7,0,!0);Ze(h,3,3),Ze(h,28,12)}else{for(var J of[S+3.2,S+9,F-3.2])Re(h,J,w+2,2.4,0),h.box("wood",J,.4,Y,1.1,.06,.65,0,!0);Re(h,D,N-1.2,3.4,Math.PI),Ze(h,F-.8,w+.8)}else if(_.kind==="dining"){for(var J=S+3;J<F-2;J+=4.8)for(var K=w+2.4;K<N-1.6;K+=3.7)Math.round(J)%3===0?(h.box("wood",J,.74,K,1.1,.07,.9,0,!0),Te(h,J,K-.85,Math.PI),Te(h,J,K+.85,0)):Ie(h,J,K,!0);h.box("wood",D,.94,N-.65,14,.09,.65,0,!0);for(var J=D-6;J<D+6;J+=1.5)Te(h,J,N-1.5,0)}else if(_.kind==="kitchen"){var fe=_.id==="G-KITCH"?54:D,te=Math.min(4,F-S-1);h.box("metal",fe,.86,Y,te,.1,.8,0,!0),h.box("metal",fe,.42,Y,te-.1,.75,.7,0,!0),h.box("metal",fe,2.8,Y,Math.min(4.4,F-S-.5),.55,1.1,0,!0),h.box("chair",fe,.96,Y,_.layoutVariant%2?.5:.9,.035,.5,0,!0),_.id==="G-KITCH"&&(Se(h,51,31,2),h.box("metal",54,.88,37,4,.08,.8,0,!0),h.box("metal",56.3,1,37,.9,1.9,.8,0,!0))}else if(_.kind==="toilet")if(_.id.endsWith("WC-A"))h.box("wall",S+.9,.5,N-1,.5,.5,.6,0,!0),h.box("metal",F-.6,.84,w+.7,.65,.12,.45,0,!0);else for(var J=S+.8;J<F-.5;J+=1.35)h.box("wall",J,.5,N-.8,.4,.5,.55,0,!0),h.box("metal",J,.85,w+.55,.65,.12,.45,0,!0);else if(_.kind==="pantry")Se(h,D,N-.45,F-S-.5),h.box("metal",S+1,.95,N-.45,.7,.05,.45,0,!0),h.box("wood",D,.9,Y,2,.08,.65,0,!0),Te(h,D-.5,w+.7,0),Te(h,D+.5,w+.7,0);else if(_.kind==="service")if(_.id.includes("IT"))for(var J of[S+.65,F-.65])h.box("frame",J,1,Y,.6,1.9,.8,0,!0);else if(_.id==="G-WASH")h.box("metal",D,.88,w+.7,3,.08,.8,0,!0),h.box("metal",F-1,.6,N-1,1,1.1,1,0,!0);else for(var J=S+1;J<F-.8;J+=1.8)Se(h,J,N-.65,1.3);else if(_.kind==="stair")for(var pe=0;pe<12;pe++)h.box("concrete",D,.09+pe*.18,w+.4+pe*.25,2,.18,.25,0,!0)}function W(h,_){var v=_.rect,S=(v[0]+v[2])/2,w=(v[1]+v[3])/2,F=v[2]-v[0],N=v[3]-v[1];function D(pe,ze,Ue,at){return!we(_.floor).some(function(on){return pe-Ue/2<on.box[3]+.08&&pe+Ue/2>on.box[0]-.08&&ze-at/2<on.box[4]+.08&&ze+at/2>on.box[1]-.08})}if(_.kind==="meeting"){for(var Y=_.people_assumed>12?3:2,J=0;J<Y;J++){var K=w+(J-(Y-1)/2)*2.8;D(S,K,3,3)&&Ie(h,S,K,!0)}h.box("screen",S,1.75,v[1]+.2,1.8,1,.06,0,!0)}else if(_.function==="Executive")D(S,w-2,1.7,2.4)&&oe(h,S,w-2,Math.PI),Re(h,S,w+2,2.8,0),Se(h,S,v[1]+.6,Math.min(3,F-1));else if(_.function==="Reception")h.box("wood",S,.95,v[1]+1.5,Math.min(3.5,F-1),.12,.75,0,!0),Re(h,S,w+1.4,Math.min(3,F-1),0),Ze(h,v[0]+.8,v[1]+.8);else if(_.kind==="office")for(var fe=0,K=v[1]+1.8;K<v[3]-1.7;K+=2.6)for(var te=v[0]+1.2;te<v[2]-1.1&&!(fe>=_.people_assumed);te+=2.6)D(te,K,1.5,2.3)&&(oe(h,te,K,_.tenant==="A"?0:Math.PI),fe++);else if(_.kind==="pantry")Se(h,S,v[1]+.6,F-.8),h.box("metal",v[0]+.8,.94,v[1]+.6,.7,.06,.48,0,!0),h.box("metal",v[2]-.7,1,v[1]+.65,.65,1.9,.65,0,!0),D(S,w+1,3,2.8)&&Ie(h,S,w+1,!0);else if(_.kind==="toilet"){for(var K=v[1]+1.5;K<v[3]-.7;K+=2.5)h.box("wall",v[2]-.85,.45,K,.55,.55,.7,0,!0),h.box("wall",v[2]-1.55,1.05,K,.08,2.1,1.5,0,!0);h.box("metal",v[0]+.55,.84,w,.7,.12,.48,0,!0)}else if(_.kind==="janitor")Se(h,S,v[3]-.6,F-.7),h.box("metal",v[0]+.65,.4,v[1]+.9,.65,.8,.6,0,!0),h.box("chair",v[2]-.7,.65,w,.65,1.1,.6,0,!0);else if(_.function==="IT"){for(var te=v[0]+.8;te<v[2]-.5;te+=1.3)D(te,v[3]-1.1,.75,1.2)&&h.box("frame",te,1.05,v[3]-1.1,.65,2,.8,0,!0);Se(h,S,v[1]+.6,Math.min(3,F-1))}}window.__SEAT_AUDIT=[];function Te(h,_,v,S,w){window.__SEAT_AUDIT.push({room:window.__FURNISH_ROOM,position:[_,v],angle:S||0,front:[Math.sin(S||0),-Math.cos(S||0)],target:w||null});var F=S||0,N=Math.cos(F),D=Math.sin(F);function Y(te,pe,ze,Ue,at,on,dt,Rn){h.box(te,_+pe*N-Ue*D,ze,v+pe*D+Ue*N,at,on,dt,F+(Rn||0),!0)}Y("chair",0,.47,0,.47,.11,.45),Y("chair",0,.73,.18,.44,.48,.07),Y("frame",0,.29,0,.045,.28,.045);for(var J=0;J<5;J++){var K=J*Math.PI*2/5;Y("metal",Math.sin(K)*.12,.16,Math.cos(K)*.12,.035,.035,.27,K),Y("frame",Math.sin(K)*.24,.095,Math.cos(K)*.24,.065,.1,.045,K)}for(var fe of[-.27,.27])Y("frame",fe,.56,.05,.028,.19,.035),Y("chair",fe,.66,.01,.06,.035,.28);Y("frame",0,.58,.19,.08,.32,.025)}function oe(h,_,v,S){var w=S||0,F=Math.cos(w),N=Math.sin(w);function D(Y,J,K,fe,te,pe,ze){h.box(Y,_+J*F-fe*N,K,v+J*N+fe*F,te,pe,ze,w,!0)}D("wood",0,.75,0,1.45,.055,.72),D("frame",-.57,.38,0,.045,.71,.6),D("frame",.57,.38,0,.045,.71,.6),D("metal",0,.69,0,1.14,.045,.045),D("screen",0,1.03,-.13,.49,.29,.024),D("metal",0,.85,-.13,.055,.18,.045),D("frame",0,.78,-.13,.18,.025,.12),D("frame",-.08,.793,.14,.4,.018,.14),D("chair",.28,.795,.14,.055,.024,.09),D("wall",.57,.79,-.18,.09,.055,.09),Te(h,_-Math.sin(w)*.73,v+Math.cos(w)*.73,w,[_,v]),D("wall",-.49,.38,-.03,.28,.57,.55),D("metal",-.49,.48,.26,.14,.015,.018),D("metal",-.49,.25,.26,.14,.015,.018)}function Re(h,_,v,S,w){var F=w||0,N=Math.cos(F),D=Math.sin(F);function Y(te,pe,ze,Ue,at,on,dt){h.box(te,_+pe*N-Ue*D,ze,v+pe*D+Ue*N,at,on,dt,F,!0)}Y("frame",0,.18,0,S-.12,.15,.72),Y("sofa",0,.72,-.35,S-.12,.64,.15);for(var J=0;J<3;J++)Y("sofa",(J-1)*(S-.35)/3,.4,.02,(S-.35)/3-.02,.22,.65);for(var K of[-S/2+.08,S/2-.08])Y("sofa",K,.51,0,.16,.48,.85);for(var K of[-S*.4,S*.4])for(var fe of[-.27,.27])Y("metal",K,.085,fe,.045,.12,.045)}var He=W;W=function(h,_){if(!_.r7)return He(h,_);var v=_.rect,S=(v[0]+v[2])/2,w=(v[1]+v[3])/2;if(_.kind==="lobby"){for(var F of[v[0]+3.2,v[2]-3.2])Re(h,F,w-2.3,2.8,0),h.box("wood",F,.4,w-.9,1.2,.06,.7,0,!0),Te(h,F-.95,w+.8,Math.PI),Te(h,F+.95,w+.8,Math.PI);Ze(h,v[0]+.9,v[1]+.9),Ze(h,v[2]-.9,v[1]+.9),Se(h,S,v[1]+.65,3.6);return}if(_.kind==="meeting"){var N=_.people_assumed,D=N>=12?5:3.8,Y=w-.7;h.box("wood",S,.76,Y,1.28,.065,D,0,!0);for(var J of[-D*.38,D*.38])h.box("frame",S,.37,Y+J,.75,.72,.075,0,!0);for(var K=0;K<(N-2)/2;K++){var fe=Y+(K-((N-2)/2-1)/2)*.86;Te(h,S-.94,fe,Math.PI/2,[S,Y]),Te(h,S+.94,fe,-Math.PI/2,[S,Y])}Te(h,S,Y-D/2-.6,Math.PI,[S,Y]),Te(h,S,Y+D/2+.6,0,[S,Y]),h.box("screen",S,1.7,v[1]+.12,2,1.1,.055,0,!0),Se(h,S,v[1]+.45,3.2),Ze(h,v[2]-.75,v[1]+.8);return}He(h,_),_.function==="Open office"&&(h.box("wood",v[0]+2.3,.4,v[3]-1.6,1,.06,.65,0,!0),Ze(h,v[0]+.8,v[3]-.8),h.box("wall",S,.92,v[1]+3.1,Math.min(8,v[2]-v[0]-2),.32,.045,0,!0)),_.function==="Executive"&&(h.box("wall",S,1.6,v[1]+.12,2,.7,.04,0,!0),Ze(h,v[0]+.8,v[3]-1)),_.function==="Reception"&&(h.box("wood",S,.38,w+2.3,1.2,.055,.65,0,!0),h.box("wall",v[0]+.15,1.65,w,.04,.6,2.8,0,!0)),_.kind==="pantry"&&(h.box("frame",v[0]+1.5,1.12,v[1]+.6,.38,.3,.32,0,!0),h.box("glass",v[0]+2.2,1.05,v[1]+.6,.08,.18,.08,0,!0))};var ve=W;W=function(h,_){window.__FURNISH_ROOM=_.id,ve(h,_),window.__FURNISH_ROOM=null};function st(h,_){for(var v of["CHS","CHR"]){var S=[],w=[],F=[],N=[],D=n.cyl(1,1,10),Y=D.attributes.position,J=D.attributes.normal,K=D.attributes.uv,fe=D.index;if(xe.waterPipes.filter(function(pe){return pe.floor===h&&pe.service===v}).forEach(function(pe){pe.points.slice(1).forEach(function(ze,Ue){var at=pe.points[Ue],on=new y(ze[0]-at[0],ze[2]-at[2],at[1]-ze[1]),dt=on.length();if(!(dt<.001)){for(var Rn=new rn().setFromUnitVectors(new y(0,1,0),on.normalize()),Xi=new y((at[0]+ze[0])/2,(at[2]+ze[2])/2,-(at[1]+ze[1])/2),ps=S.length/3,Ht=0;Ht<Y.count;Ht++){var qi=new y(Y.getX(Ht)*pe.outsideRadius_m,Y.getY(Ht)*dt,Y.getZ(Ht)*pe.outsideRadius_m).applyQuaternion(Rn).add(Xi);S.push(qi.x,qi.y,qi.z);var Ds=new y(J.getX(Ht),J.getY(Ht),J.getZ(Ht)).applyQuaternion(Rn);w.push(Ds.x,Ds.y,Ds.z),F.push(K.getX(Ht),K.getY(Ht))}for(var Ht=0;Ht<fe.count;Ht++)N.push(ps+fe.getX(Ht))}})}),S.length){var te=new _t(1,1,1);te.setAttribute("position",new Y.constructor(S,3)),te.setAttribute("normal",new J.constructor(w,3)),te.setAttribute("uv",new K.constructor(F,2)),te.setIndex(N),te.clearGroups(),te.computeBoundingSphere(),n.mesh(te,new ge({color:v==="CHS"?"#1559d6":"#57c5f5",roughness:.55,metalness:.35,envMapIntensity:.04}),_)}D.dispose()}}function Je(h,_,v,S){if(re(_,h,28,27,36,27,3.45),re(_,h,28,39,36,39),re(_,h,28,27,28,39),re(_,h,36,27,36,39),xe.verticalTransport.lifts.forEach(function(N){var D=N.rect;re(_,h,D[0],D[1],D[2],D[1]),re(_,h,D[0],D[1],D[0],D[3]),re(_,h,D[2],D[1],D[2],D[3]),re(_,h,D[0],D[3],D[2],D[3],(D[2]-D[0])/2-.55),v.box("metal",(D[0]+D[2])/2,1.15,D[3]-.045,1.1,2.25,.035),v.box("screen",D[2]-.2,1.55,D[3]+.1,.1,.16,.025),ce(S,N.id,(D[0]+D[2])/2,.075,D[3]+.6,2.8)}),ce(S,"LIFT LOBBY",32,.075,36.4,5),xe.verticalTransport.fireStairs.forEach(function(N){var D=N.rect,Y=(D[0]+D[2])/2,J=(D[1]+D[3])/2,K=D[2]-D[0];v.box("tile",Y,.025,J,K,.04,D[3]-D[1]),re(_,h,D[0],D[1],D[2],D[1]),re(_,h,D[0],D[3],D[2],D[3]),re(_,h,D[0],D[1],D[0],D[3],N.id==="FS-E"?.45:void 0),re(_,h,D[2],D[1],D[2],D[3],N.id==="FS-W"?.95:void 0);for(var fe=Math.ceil(E(h)/.18),te=Math.ceil(fe/2),pe=E(h)/fe,ze=.28,Ue=0;Ue<te;Ue++)v.box("concrete",Y-.95,pe*(Ue+.5),D[1]+.5+Ue*ze,1.5,pe,ze);v.box("concrete",Y,E(h)/2-.09,D[1]+.5+te*ze,3.8,.18,1);for(var Ue=0;Ue<fe-te;Ue++)v.box("concrete",Y+.95,E(h)/2+pe*(Ue+.5),D[1]+.5+(te-Ue-1)*ze,1.5,pe,ze);ce(S,N.id+" / FIRE EXIT",Y,.075,D[3]-.5,3.7)}),h>1){for(var w of[24.5,39.5]){for(var F of[[.5,13.7],[16.8,22.7],[25.3,28.7],[31,39.5]])re(_,h,w,F[0],w,F[1]);for(var F of[[13.7,16.8,1],[22.7,25.3,.75],[28.7,31,.6]])re(_,h,w,F[0],w,F[1],F[2],!0)}ce(S,"COMPANY A / 888.69 m\xB2",12,.075,15.4,9),ce(S,"COMPANY B / 888.69 m\xB2",52,.075,15.4,9)}(xe.corridors||[]).filter(function(N){return N.floor===h}).forEach(function(N){var D=N.rect;v.box("tile",(D[0]+D[2])/2,.056,(D[1]+D[3])/2,D[2]-D[0],.018,D[3]-D[1])})}n.LAYER.shell.clear(),n.LAYER.interiors=new Oe,n.LAYER.ducts=new Oe,n.scene.add(n.LAYER.interiors,n.LAYER.ducts);for(var Xt of Array.from(n.LAYER.plant.children))Xt.userData.eq||n.LAYER.plant.remove(Xt);for(var De=0;De<=9;De++){var On=new Oe,Jn=new Oe,uo=new Oe,fo=new Oe,Vi=new Oe,wr=new Oe,po=new Oe,mo=new Oe;On.position.y=Jn.position.y=uo.position.y=fo.position.y=Vi.position.y=po.position.y=$(De),n.LAYER.shell.add(On,Jn),n.LAYER.interiors.add(uo,fo,Vi,po),n.LAYER.ducts.add(wr,mo);var go=new Oe,zi=new Oe;On.add(go,zi),Rt[De]={structural:On,slab:zi,facade:Jn,interior:uo,walls:fo,names:Vi,ducts:wr,lighting:po,water:mo,beams:go},st(De,mo);var Ai=Ae(On,De,"structure"),_o=Ae(zi,De,"structure"),Sa=Ae(go,De,"structure"),si=Ae(Jn,De,"envelope"),Gi=Ae(uo,De,"furniture"),Tn=Ae(fo,De,"wall"),qt=Ae(wr,De,"duct",!0),Ar=Ae(po,De,"lights"),Xl=De===0?[]:xe.shafts.map(function(h){return h.rect}).concat(xe.verticalTransport.lifts.map(function(h){return h.rect})),cs=[0,64],hs=[0,40];Xl.forEach(function(h){cs.push(h[0],h[2]),hs.push(h[1],h[3])}),cs=[...new Set(cs)].sort(function(h,_){return h-_}),hs=[...new Set(hs)].sort(function(h,_){return h-_});for(var tr=0;tr<cs.length-1;tr++)for(var Ps=0;Ps<hs.length-1;Ps++){var R=(cs[tr]+cs[tr+1])/2,G=(hs[Ps]+hs[Ps+1])/2;Xl.some(function(h){return R>h[0]&&R<h[2]&&G>h[1]&&G<h[3]})||_o.box("concrete",R,-.14,G,cs[tr+1]-cs[tr],.28,hs[Ps+1]-hs[Ps])}if(De<9){var ie=E(De)-.25;if(xe.columns.filter(function(h){return h.floor===De}).forEach(function(h){Ai.box("concrete",(h.box[0]+h.box[3])/2,ie/2,(h.box[1]+h.box[4])/2,.6,ie,.6)}),xe.beams.filter(function(h){return h.floor===De}).forEach(function(h){Sa.box("concrete",(h.box[0]+h.box[3])/2,(h.box[2]+h.box[5])/2-$(De),(h.box[1]+h.box[4])/2,h.box[3]-h.box[0],.55,h.box[4]-h.box[1])}),De>0){for(var j of[0,40]){si.box("frame",32,.3,j,64,.6,.13),si.box("frame",32,ie-.2,j,64,.4,.13);for(var Z=0;Z<=64;Z+=2)si.box("frame",Z,ie/2,j,.055,ie,.12);j===40&&si.box("glass",32,ie/2,j,64,ie-.65,.02)}for(var j of[0,64]){si.box("frame",j,.3,20,.13,.6,40),si.box("frame",j,ie-.2,20,.13,.4,40);for(var Le=0;Le<=40;Le+=2)si.box("frame",j,ie/2,Le,.12,ie,.055);j===0&&si.box("glass",j,ie/2,20,.02,ie-.65,40)}}}if(De===0){Gi.box("tile",32,.025,20,63.8,.035,39.8),re(Tn,0,50,18,63.5,18,7),re(Tn,0,50,26,63.5,26),re(Tn,0,50,18,50,26),re(Tn,0,63.5,18,63.5,26),ce(Vi,"B1 \xB7 CHILLER PLANT",24,.075,22,15),ce(Vi,"ELECTRICAL",57,.075,25,7);for(var Z=3;Z<48;Z+=8)Gi.box("SA",Z,.055,18,.06,.02,5),Gi.box("SA",Z+2,.055,18,.06,.02,5);for(var Z=6;Z<62;Z+=8)Ar.box("luminaire",Z,4.65,18,3.2,.045,.08);for(var Z=4;Z<45;Z+=8)Ar.box("luminaire",Z,4.65,11,3.2,.045,.08)}else if(De<9)Gi.box("tile",32,.025,20,63.8,.03,39.8),vt.filter(function(h){return h.floor===De}).forEach(function(h){var _=h.rect,v=_[0],S=_[1],w=_[2],F=_[3],N=(v+w)/2,D=(S+F)/2;Gi.box(h.kind==="office"?"carpet":h.kind==="meeting"?"wood":"tile",N,.049,D,w-v-.12,.026,F-S-.12);var Y=h.doorSide||(D<18?"north":"south"),J=h.kind==="office"||h.kind==="meeting";if(re(Tn,De,v,S,w,S,Y==="south"?h.doorCenter?h.doorCenter[0]-v-.55:(w-v)/2-.55:void 0,J),re(Tn,De,v,F,w,F,Y==="north"?h.doorCenter?h.doorCenter[0]-v-.55:(w-v)/2-.55:void 0,J),re(Tn,De,v,S,v,F),re(Tn,De,w,S,w,F),ce(Vi,h.name,N,.075,h.id.endsWith("EN3")&&h.kind==="mechanical"?31.5:D,Math.min(5,w-v-.3)),h.kind==="office"&&De>1&&v<40&&!h.r6){var K=D<18?F-h.privateDepth_m:S+h.privateDepth_m;re(Tn,De,v,K,w,K,(w-v)/2-.55,!0)}xt(Gi,h);for(var fe=S+1.2;fe<F-.5;fe+=3.2)Ar.box("luminaire",N,3.22,fe,Math.min(3.2,w-v-.8),.04,.055,0,!0)}),xe.shafts.forEach(function(h){var _=h.rect;re(Tn,De,_[0],_[1],_[2],_[1]),re(Tn,De,_[0],_[3],_[2],_[3]),re(Tn,De,_[0],_[1],_[0],_[3]),re(Tn,De,_[2],_[1],_[2],_[3],.8)});else{Ai.box("concrete",44,1.75,21,8,3.5,12),Ai.box("frame",19.6,.9,6,34.5,.2,3);for(var Z=0;Z<64;Z+=4)Ai.box("frame",Z,.015,20,.012,.02,40);for(var Le=0;Le<40;Le+=4)Ai.box("frame",32,.015,Le,64,.02,.012);Ai.box("frame",32,.45,40,64,.9,.12),Ai.box("frame",0,.45,20,.12,.9,40)}(xe.ductBodies||xe.ducts).filter(function(h){return h.floor===De}).forEach(function(h){if(h.points.slice(1).forEach(function(w,F){var N=h.points[F],D=N[2]!==w[2],Y=Math.hypot(w[0]-N[0],w[1]-N[1],w[2]-N[2]),J=(N[0]+w[0])/2,K=(N[1]+w[1])/2,fe=(N[2]+w[2])/2,te=N[1]===w[1];if(xe.ductShells||qt.box(h.service==="RA"?"returnDuct":"duct",J,fe,K,D?h.w:te?Y:h.w,D?Y:h.h,D?h.h:te?h.w:Y,0,!1),!D)for(var pe=1;pe<Y;pe+=2.4){var ze=N[0]+(w[0]-N[0])*pe/Y,Ue=N[1]+(w[1]-N[1])*pe/Y;qt.box("frame",ze,fe,Ue,te?.025:h.w+.035,h.h+.028,te?h.w+.035:.025,0,!0);var at=fe+h.h/2+.015,on=Math.min($(De)+E(De)-.835,at+.12);if(on>at)for(var dt of[-1,1])qt.box("metal",ze+(te?0:dt*(h.w/2+.08)),(at+on)/2,Ue+(te?dt*(h.w/2+.08):0),.014,on-at,.014,0,!0);pe===1&&qt.box(h.service,ze,fe+h.h/2+.022,Ue,te?.2:h.w,.02,te?h.w:.2)}}),De===1&&(h.id.startsWith("OA-to-")||h.id.startsWith("FCU-SA-")||h.id.startsWith("PRIVATE-SA-")||h.id.startsWith("PRIVATE-OA-"))){var _=h.points[h.points.length-1];qt.box("metal",_[0],_[2]-.18,_[1],.6,.055,.6,0,!0);for(var v of[.46,.33,.2])qt.box("wall",_[0],_[2]-.14,_[1]-v/2,v,.02,.025,0,!0),qt.box("wall",_[0],_[2]-.14,_[1]+v/2,v,.02,.025,0,!0);qt.box("SA",_[0],_[2]-.12,_[1],.12,.02,.12,0,!0)}if(De===1&&(h.id.startsWith("RA-F")||h.id.startsWith("TE-F")||h.id.startsWith("PRIVATE-RA-"))){var _=h.points[0];qt.box("frame",_[0],_[2]-.15,_[1],.5,.035,.5,0,!0);for(var S=-.18;S<.2;S+=.06)qt.box("metal",_[0],_[2]-.12,_[1]+S,.45,.015,.024,0,!0)}}),(xe.diffusers||[]).filter(function(h){return h.floor===De}).forEach(function(h){var _=h.position,v=h.face_m[0],S=h.face_m[1];if(h.service==="TA"){qt.box("metal",_[0],_[2],_[1],v,S,.04,0,!0);for(var w=-S*.4;w<S*.4;w+=.04)qt.box("frame",_[0],_[2]+w,_[1]+.025,v*.9,.015,.02,0,!0);return}if(qt.box("metal",_[0],_[2],_[1],v,.045,S,0,!0),h.service==="SA"||h.service==="OA")for(var F of[.8,.58,.36])qt.box("wall",_[0],_[2]-.025,_[1]-S*F/2,v*F,.025,.025,0,!0),qt.box("wall",_[0],_[2]-.025,_[1]+S*F/2,v*F,.025,.025,0,!0),qt.box("wall",_[0]-v*F/2,_[2]-.025,_[1],.025,.025,S*F,0,!0),qt.box("wall",_[0]+v*F/2,_[2]-.025,_[1],.025,.025,S*F,0,!0);else for(var F=-S*.4;F<S*.4;F+=.065)qt.box("frame",_[0],_[2]-.03,_[1]+F,v*.85,.025,.02,0,!0)}),[].forEach(function(h){var _=h.position,v=h.size[0],S=h.size[1],w=h.size[2];if(qt.box("metal",_[0],_[2]+w/2,_[1],v,w,S,0,!0),qt.box("insulated",_[0],_[2]+w*.55,_[1]+S/2+.015,v*.7,w*.6,.025,0,!0),qt.box("frame",_[0],_[2]-.035,_[1],v+.1,.035,S+.08,0,!0),h.floor===9){for(var F=_[0]-v/2+.5;F<_[0]+v/2;F+=.7)qt.box("frame",F,_[2]+w/2,_[1]+S/2+.02,.025,w,.04,0,!0),qt.box("metal",F+.15,_[2]+w*.55,_[1]+S/2+.05,.04,.28,.035,0,!0);qt.box("frame",_[0],_[2]+w+.04,_[1],v+.16,.06,S+.16);for(var N=_[1]-S/2+.12;N<_[1]+S/2;N+=.11)qt.box("frame",_[0]+v/2+.02,_[2]+w*.5,N,.04,w*.65,.028)}}),De<9?Je(De,Tn,Gi,Vi):xe.verticalTransport.fireStairs.forEach(function(h){var _=h.rect;_o.box("concrete",(_[0]+_[2])/2,-.14,(_[1]+_[3])/2,_[2]-_[0],.28,_[3]-_[1]),ce(Vi,h.id+" ROOF EXIT",(_[0]+_[2])/2,.075,_[3]-.4,3.8)}),Ai.flush(),_o.flush(),Sa.flush(),si.flush(),Gi.flush(),Tn.flush(),qt.flush(),Ar.flush()}var Ye=function(h){var _=new _t(1,1,1),v=_.attributes.position.constructor;_.setIndex(null),_.clearGroups(),_.setAttribute("position",new v(new Float32Array(h.positions),3)),_.deleteAttribute("uv"),_.deleteAttribute("normal"),_.computeVertexNormals(),_.computeBoundingSphere();var S=new ge({color:h.service==="RA"?"#a4a9a6":"#b1bfc3",metalness:.12,roughness:.6,transparent:!0,opacity:.19,depthWrite:!1,side:mn}),w=n.mesh(_,S,Rt[h.floor].ducts);w.userData.designKind="duct",w.userData.service=h.service,w.renderOrder=8};xe.ductShells?xe.ductShells.forEach(Ye):xe.ductShellsBin&&fetch(window.ALT_URL("alt79/"+xe.ductShellsBin.src)).then(function(h){if(!h.ok)throw Error("HTTP "+h.status);return h.arrayBuffer()}).then(function(h){var _=xe.ductShellsBin,v=new Float32Array(h,0,_.nv*3),S=new Uint16Array(h,_.nv*12),w=0,F=0;_.items.forEach(function(N){for(var D=new Float32Array(N[3]*3),Y=0;Y<N[3];Y++){var J=(w+S[F+Y])*3;D[Y*3]=v[J],D[Y*3+1]=v[J+1],D[Y*3+2]=v[J+2]}Ye({floor:N[0],service:N[1],positions:D}),w+=N[2],F+=N[3]}),n.applyFloor()}).catch(function(h){console.warn("duct shells not loaded",h)});for(var De=0;De<=8;De++)for(var Ne of[[18,10],[18,33],[55,8],[55,33]]){var Ke=new Di(16769717,180,26,2);Ke.position.set(Ne[0],De===0?4.8:3.25,-Ne[1]),Rt[De].lighting.add(Ke)}for(var Z of[4,12,20,28,36,44]){var Ke=new Di(14084607,260,15,2);Ke.position.set(Z,4.5,-10),Rt[0].lighting.add(Ke)}for(var $e in n.EQ){var We=n.EQ[$e];if(We.mats.forEach(function(h){h.isMeshStandardMaterial&&(h.envMapIntensity=.05)}),We.e.type==="chiller"&&(We.parts.evap&&We.parts.evap.material.color.set("#3f4b4f"),We.parts.cond&&We.parts.cond.material.color.set("#aab4b5")),We.e.type==="pump"&&We.mats.forEach(function(h){h.color&&h.color.getHexString()==="345e73"&&h.color.set("#315e7b")}),We.e.type==="ahu"){We.mats.forEach(function(h){h.color&&h.color.getHexString()==="d2d8d7"&&h.color.set("#a8b8b1")});for(var j of[-1,1])n.mesh(n.box(.16,.6,.9),lt.duct,We.g,new y(j*(n.mm(We.e.L)/2+.08),n.mm(We.e.H)*.62,0))}}for(var $e in n.EQ){var We=n.EQ[$e];if(We.parts.evap){var yt=We.parts.evap.material.clone();yt.color.set("#2c3d42"),yt.metalness=.08,yt.roughness=.85,We.parts.evap.material=yt,We.mats.add(yt)}}n.svcMat.CHS.color.set("#1559d6"),n.svcMat.CHR.color.set("#57c5f5"),n.svcMat.CDS.color.set("#efc72f"),n.svcMat.CDR.color.set("#ed781c");for(var je in n.svcMat)n.svcMat[je].envMapIntensity=.035;var kt={CHS:"#1559d6",CHR:"#57c5f5",CDS:"#efc72f",CDR:"#ed781c"};for(var $e in n.PIPE){var Pt=n.PIPE[$e],Qt=kt[Pt.p.svc];Qt&&(Pt.mat.color.set(Qt),Pt.mat.envMapIntensity=.05,Pt.mat.roughness=.48,Pt.oc=Pt.mat.color.clone(),n.svcMat[Pt.p.svc+"_band"].color.set(xe.pipeColors[Pt.p.svc]))}for(var $e in n.EQ){var We=n.EQ[$e];if(We.e.type==="ahu"&&(n.mesh(n.box(.8,.25,.18),lt.duct,We.g,new y(0,1.47,n.mm(We.e.W)/2+.08)),We.e.floor<9))for(var Vt of[[-.9,1.5],[-1.3,.9]])n.mesh(n.cyl(.065,.16,14),lt.blue,We.g,new y(Vt[0],Vt[1],-.95),[Math.PI/2,0,0]),n.mesh(n.cyl(.11,.03,16),lt.metal,We.g,new y(Vt[0],Vt[1],-1.015),[Math.PI/2,0,0])}var Mt=document.createElement("div");Mt.className="office-controls",Mt.innerHTML='<h2>Office / Food court \xB7 R3</h2><label><input data-layer="interiors" type="checkbox" checked> Rooms / furniture / lighting</label><label><input data-layer="ducts" type="checkbox" checked> AHU duct / VAV / damper</label><label><input id="officeNames" type="checkbox"> Room names</label><label>Wall cutaway <select id="officeWalls"><option value="0.43">Low 1.25 m</option><option value="1">Full 2.9 m</option></select></label><label>Lighting <select id="officeTheme"><option value="dusk">Dusk \xB7 warm light</option><option value="day">Day \xB7 real materials</option><option value="night">Night \xB7 building section</option></select></label><small>Coordinated concept \xB7 B1 plant<br>AHU VAV / hood / MAU points per the r6 layer</small>',document.querySelector("aside section").appendChild(Mt),Mt.querySelectorAll("label").forEach(function(h){h.style.display="block",h.style.margin="7px 0"}),Mt.insertAdjacentHTML("afterbegin",'<label><input id="officeSection" type="checkbox"> Open the ground floor to see B1 (columns / beams kept)</label>'),Mt.insertAdjacentHTML("beforeend",'<label><input id="officeWater" type="checkbox" checked> CHW piping to AHU / PICV</label>'),Mt.insertAdjacentHTML("beforeend",'<label><input id="officeBeams" type="checkbox" checked> Show beams</label>'),Mt.querySelectorAll("label").forEach(function(h){h.style.display="block",h.style.margin="7px 0"});var Xe=new Bn(new y(0,0,-1),-14);n.scene.children.forEach(function(h){Math.abs(h.position.y+.29)<.002&&h.isMesh&&(h.visible=!1),h.position.z===22&&Math.abs(h.position.y+.3)<.002&&(h.visible=!1)});function Sn(){var h=n.$("officeTheme").value;n.sky.visible=!1,n.scene.background=new ke(h==="day"?"#bdc9cd":h==="dusk"?"#233b4b":"#0d2132"),n.scene.fog=null,n.sun.position.set(45,95,35),n.sun.intensity=h==="day"?2.5:h==="dusk"?1.3:.65,n.sun.color.set("#fff4de"),n.hemi.intensity=h==="day"?1.7:h==="dusk"?1.25:.9,n.hemi.color.set("#d4e0e5"),n.hemi.groundColor.set("#8a8070"),n.renderer.toneMappingExposure=h==="day"?1.05:h==="dusk"?1.15:1.2}var Ot=n.applyWeather;n.applyWeather=function(h,_){Ot(h,_),Sn()},n.$("officeTheme").addEventListener("change",Sn),Sn(),n.$("labelsOn").checked=!1,n.$("labelsOn").dispatchEvent(new Event("change")),n.LAYER.zones.visible=!1;var Qn=document.querySelector('[data-layer="zones"]');Qn.checked=!0,n.LAYER.zones.visible=!0,Qn.parentElement.lastChild.textContent=" Room colours \xB7 Temperature / RH / CO\u2082",n.$("fsel").insertAdjacentHTML("afterbegin",'<option value="0">B1 \xB7 Chiller plant</option>');function mi(h){return!h.e.slot||n.isInst(h.e.slot,n.M.installed[h.e.slot])}function us(h){return h.e.floor!==void 0?h.e.floor:h.e.type==="ct"?9:0}function hn(h){return n.FSEL==="all"||n.FSEL==="roof"?n.FSEL==="all"||h===9:n.ISO?h===+n.FSEL:h<=+n.FSEL}n.applyFloor=function(){var h=/^\d+$/.test(n.FSEL),_=h&&n.ISO,v=h?$(+n.FSEL)-.3:-7,S=h?$(+n.FSEL)+E(+n.FSEL)-.2:40,w=_?[new Bn(new y(0,1,0),-v),new Bn(new y(0,-1,0),S)]:null;n.LAYER.plant.visible=n.LAYCHK("plant"),n.LAYER.piping.visible=n.LAYCHK("piping"),n.LAYER.air.visible=n.LAYCHK("air"),n.LAYER.interiors.visible=n.LAYCHK("interiors"),n.LAYER.ducts.visible=n.LAYCHK("ducts");for(var F in Rt){var N=Rt[F],D=hn(+F);N.structural.visible=N.interior.visible=N.walls.visible=N.lighting.visible=N.ducts.visible=D,N.facade.visible=D&&!_,N.names.visible=D&&n.$("officeNames").checked,N.walls.scale.y=_?+n.$("officeWalls").value:1,N.beams.visible=n.$("officeBeams").checked;var Y=0;N.lighting.children.forEach(function(Ue){Ue.isPointLight&&(Ue.visible=_||+F==0||Y===0||Y===3,Y++)}),N.water.visible=D&&n.$("officeWater").checked,["structural","facade","interior","walls","lighting","ducts","water"].forEach(function(Ue){N[Ue].traverse(function(at){at.isMesh&&at.material&&(at.material.clippingPlanes=null)})}),+F==1&&n.FSEL==="all"&&n.$("officeSection").checked&&(N.slab.traverse(function(Ue){Ue.isMesh&&(Ue.material.clippingPlanes=[Xe])}),N.interior.children.forEach(function(Ue){Ue.isMesh&&Ue.material.color.getHexString()===lt.tile.color.getHexString()&&(Ue.material.clippingPlanes=[Xe])})),+F==9&&_&&(N.ducts.visible=!0,N.ducts.traverse(function(Ue){Ue.isMesh&&Ue.material&&(Ue.material.clippingPlanes=w)}))}for(var J in n.EQ){var K=n.EQ[J];K.g.visible=hn(us(K))&&(mi(K)||n.$("showSpare").checked),n.LBL[J]&&(n.LBL[J].dataset.hidden=K.g.visible&&K.g.parent.visible?"":"1")}n.renderer.localClippingEnabled=!0;for(var J in n.PIPE){var fe=n.PIPE[J],te=fe.p.pts.map(function(at){return n.mm(at[2])}),pe=!_||Math.min(...te)<=S&&Math.max(...te)>=v;fe.g.visible=pe&&(!fe.ghost||n.$("showSpare").checked)&&(n.FSEL!=="roof"||Math.max(...te)>34.8),fe.g.traverse(function(at){at.isMesh&&at.material&&(at.material.clippingPlanes=w)})}for(var ze in n.ZONE)n.ZONE[ze].g.visible=!1;n.apron.visible=n.ground.visible=!1,n.trees.forEach(function(Ue){Ue.visible=!1}),n.devicesFloor&&n.devicesFloor(hn)},Jt=function(){n.applyFloor()};function Nt(h){n.FSEL=h,n.$("fsel").value=h,n.ISO=/^\d+$/.test(h),n.$("fiso").checked=n.ISO,n.LAYER.shell.visible=!0,document.querySelector('[data-layer="shell"]').checked=!0,n.applyFloor();var _=/^\d+$/.test(h)?$(+h):h==="roof"?34.9:10;h==="all"?n.flyTo([99,37,79],[32,12,-20]):h==="0"?n.flyTo([94,39,49],[32,-3,-17]):n.flyTo([93,_+53,47],[35,_+1.3,-20])}n.$("fsel").onchange=function(h){Nt(h.target.value)},n.$("fiso").onchange=function(){n.ISO=n.$("fiso").checked,n.applyFloor()},Mt.querySelectorAll("input,select").forEach(function(h){h.addEventListener("change",n.applyFloor)}),document.querySelectorAll("[data-view]").forEach(function(h){h.onclick=function(){var _=h.dataset.view;n.$("officeBeams").checked=_!=="plant",Nt(_==="plant"||_==="pumps"||_==="room"?"0":_==="roof"?"roof":_==="floor"?"3":"all"),_==="plant"&&n.flyTo([24,8,-31],[9,-4.7,-11]),_==="pumps"&&n.flyTo([78,9,8],[56,-5,-7]),_==="room"&&n.flyTo([60,2,30],[32,-4,-11])}}),document.querySelectorAll("[data-view]").forEach(function(h){h.addEventListener("click",function(){n.LAYER.shell.visible=!0,document.querySelector('[data-layer="shell"]').checked=!0,n.applyFloor()})}),addEventListener("DOMContentLoaded",function(){n.$("navHome").onclick=function(){Nt("all")},n.$("navIn").onclick=function(){n.zoomBy(.72)},n.$("navOut").onclick=function(){n.zoomBy(1/.72)},[["navUp",1],["navDn",-1]].forEach(function(h){n.$(h[0]).onclick=function(){Nt(String(Math.max(0,Math.min(8,(+n.FSEL||0)+h[1]))))}})}),document.querySelector("header h1").textContent="ALT Office \xB7 Lobby / Food court / B1 plant",document.querySelector("header .sub").textContent="Lobby + food court / 7 rental office floors / 119 suites",document.querySelector(".material-note").textContent="EIT / ASHRAE design basis \xB7 sizing and structure still to be confirmed",n.LAYER.zones.clear();var Ct=[],Wn={},Bt={},ri={},ds=[],Ls=["#174ea6","#087f99","#21945c","#b59812","#c05b12","#b51d32"];function xo(h,_,v){if(_||typeof h!="number"||!isFinite(h))return new ke("#455564");var S=n.MRANGE[v],w=Math.max(0,Math.min(1,(h-S[0])/(S[1]-S[0])))*(Ls.length-1),F=Math.floor(w);return new ke(Ls[F]).lerp(new ke(Ls[Math.min(F+1,Ls.length-1)]),w-F)}vt.forEach(function(h){var _=Wn[h.floor];_||(_=Wn[h.floor]=new Oe,n.LAYER.zones.add(_));var v=h.legacyZone&&n.ZONE[h.legacyZone]?n.ZONE[h.legacyZone].z:null,S=[(h.heatmapRect||h.rect).slice()];if(h.kind==="mechanical"&&h.id.endsWith("EN3")&&(S[0][3]=32.4),h.floor>1&&h.kind==="office"&&h.rect[0]<40&&!h.r6){var w=h.rect,F=(w[1]+w[3])/2<18?w[3]-h.privateDepth_m:w[1]+h.privateDepth_m;S=[[w[0],w[1],w[2],F-.08],[w[0],F+.08,w[2],w[3]]]}S.forEach(function(N,D){var Y=[N[0]+.13,N[1]+.13,N[2]-.13,N[3]-.13],J=Y[2]-Y[0],K=Y[3]-Y[1],fe=new ln({color:"#455564",transparent:!0,opacity:.82,depthWrite:!1,toneMapped:!1,polygonOffset:!0,polygonOffsetFactor:-1,polygonOffsetUnits:-1}),te=n.mesh(new _t(J,.018,K),fe,_,new y((Y[0]+Y[2])/2,$(h.floor)+.087,-(Y[1]+Y[3])/2));te.castShadow=te.receiveShadow=!1;var pe={id:h.id+(S.length>1?"-"+(D+1):""),room:h,source:v,rect:Y,mesh:te,material:fe,value:null,state:"unmapped"};te.userData.roomCell=pe.id,Ct.push(pe);for(var ze of[[(Y[0]+Y[2])/2,Y[1],J,.035],[(Y[0]+Y[2])/2,Y[3],J,.035],[Y[0],(Y[1]+Y[3])/2,.035,K],[Y[2],(Y[1]+Y[3])/2,.035,K]]){var Ue=n.mesh(new _t(ze[2],.012,ze[3]),new ln({color:"#c6d5d5",transparent:!0,opacity:.75,depthWrite:!1,toneMapped:!1}),_,new y(ze[0],$(h.floor)+.1,-ze[1]));Ue.castShadow=!1}})}),Mt.insertAdjacentHTML("beforeend",'<label><input id="officeInstruments" type="checkbox" checked> Valves / TT / PT / FM / BTU</label><label><input id="officeVAV" type="checkbox" checked> VAV / airflow pickup / actuator</label><label><input id="officeDeviceTags" type="checkbox"> Device tags</label><small>Room colours: legacy aggregates by mapping<br>grey = no mapping / no value / OOS<br>Devices show LIVE values only when bound to a station point</small>'),Mt.querySelectorAll("label").forEach(function(h){h.style.display="block",h.style.margin="7px 0"}),Mt.querySelector("h2").textContent="Office / Food court \xB7 R4";var nn={body:new ge({color:"#525d60",metalness:.7,roughness:.4,envMapIntensity:.04}),flange:new ge({color:"#89979c",metalness:.75,roughness:.38,envMapIntensity:.04}),brass:new ge({color:"#8f8055",metalness:.55,roughness:.5,envMapIntensity:.04}),actuator:new ge({color:"#bb692d",roughness:.65}),screen:new ln({color:"#273f46",toneMapped:!1}),wire:new ge({color:"#354b51",roughness:.7})};function Ut(h,_,v,S,w){var F=n.mesh(h,_,v,S);return w&&F.quaternion.copy(w),F}function _b(h){var _=Bt[h.floor];_||(_=Bt[h.floor]=new Oe,n.LAYER.piping.add(_));var v=new Oe;_.add(v),v.position.set(h.position[0],h.position[2],-h.position[1]),v.userData.instrument=h.id,v.userData.relatedEquipment=h.equipment;var S=new y(h.direction[0],h.direction[2],-h.direction[1]).normalize(),w=new rn().setFromUnitVectors(new y(0,1,0),S),F=Math.min(.16,Math.max(.025,h.radius)),N=Math.abs(S.y)>.9?new y(1,0,0):new y(0,1,0),D=N.clone().multiplyScalar(F+.075),Y=new rn().setFromUnitVectors(new y(0,1,0),N);if(h.kind==="MBFV"||h.kind==="PICV"){for(var J of[-1,1])Ut(n.cyl(F*1.5,.024,14),nn.flange,v,S.clone().multiplyScalar(J*.065),w);if(Ut(n.cyl(F*1.25,.1,14),h.kind==="PICV"?nn.brass:nn.body,v,new y,w),Ut(n.cyl(.014,.15,10),nn.flange,v,D,Y),Ut(new _t(h.kind==="PICV"?.12:.16,.1,.12),nn.actuator,v,N.clone().multiplyScalar(F+.17)),h.kind==="PICV")for(var J of[-1,1])Ut(n.cyl(.012,.07,8),nn.brass,v,S.clone().multiplyScalar(J*.045).add(N.clone().multiplyScalar(F+.055)),Y)}else if(h.kind==="TT"||h.kind==="PT")Ut(n.cyl(.01,F+.11,8),nn.flange,v,N.clone().multiplyScalar((F+.11)/2),Y),Ut(h.kind==="TT"?n.cyl(.035,.06,10):new _t(.075,.07,.055),nn.body,v,N.clone().multiplyScalar(F+.12),h.kind==="TT"?Y:null);else if(h.kind==="FM")for(var J of[-1,1]){var K=S.clone().multiplyScalar(J*.11).add(N.clone().multiplyScalar(F+.015));Ut(new _t(.075,.065,.06),nn.body,v,K),Ut(new _t(.09,.015,.085),nn.actuator,v,K.clone().add(N.clone().multiplyScalar(.035)))}else if(h.kind==="BTU"){var K=N.clone().multiplyScalar(F+.18);Ut(new _t(.2,.14,.1),nn.flange,v,K),Ut(new cn(.14,.06),nn.screen,v,K.clone().add(new y(0,0,.051)))}v.updateWorldMatrix(!0,!0);var fe=new un().setFromObject(v);ds.push({id:h.id,kind:h.kind,floor:h.floor,pipe:h.pipe,equipment:h.equipment,box:[fe.min.x,-fe.max.z,fe.min.y,fe.max.x,-fe.min.z,fe.max.y]});var te=n.textSprite(h.kind,28,"#eedbb8","rgba(24,38,44,.9)");te.position.copy(v.position).add(new y(0,.42,0)),te.scale.set(1.1,.48,1),te.userData.hardwareTag=!0,te.userData.relatedEquipment=h.equipment,_.add(te)}xe.airTerminals.forEach(function(h){var _=ri[h.floor];_||(_=ri[h.floor]=new Oe,n.LAYER.ducts.add(_));var v=new Oe;_.add(v),v.position.set(h.position[0],h.position[2],-h.position[1]),v.userData.instrument=h.id;var S=h.direction[0]!==0,w=S?h.length:h.w,F=S?h.w:h.length;Ut(new _t(w,h.h+.035,F),lt.duct,v,new y);for(var N of[-1,1])Ut(new _t(S?.018:h.w+.025,h.h+.06,S?h.w+.025:.018),nn.flange,v,new y(S?N*h.length/2:0,0,S?0:N*h.length/2));Ut(new _t(.14,.09,.1),nn.actuator,v,new y(0,-h.h/2-.07,0)),Ut(n.cyl(.009,h.w*.75,8),nn.flange,v,new y(S?-.12:0,0,S?0:-.12),new rn().setFromUnitVectors(new y(0,1,0),S?new y(0,0,1):new y(1,0,0))),Ut(new _t(.065,.05,.04),nn.body,v,new y(.12,-h.h/2-.045,0)),v.updateWorldMatrix(!0,!0);var D=new un().setFromObject(v);ds.push({id:h.id,kind:"VAV",floor:h.floor,duct:h.duct,box:[D.min.x,-D.max.z,D.min.y,D.max.x,-D.min.z,D.max.y]});var Y=n.textSprite("VAV",28,"#eedbb8","rgba(24,38,44,.9)");Y.position.copy(v.position).add(new y(0,.36,0)),Y.scale.set(1.1,.48,1),Y.userData.hardwareTag=!0,_.add(Y)});var Mp=0,Ag=n.updateZones;n.updateZones=function(h){Ag(h);var _=performance.now();if(!(_-Mp<300)){Mp=_,Ct.forEach(function(w){var F=w.source,N=F?n.V[F[n.METRIC]]:null,D=F?!!n.V[F.oos]:!0;w.value=typeof N=="number"&&isFinite(N)?N:null,w.state=F?D?"oos":w.value===null?"missing":"aggregate":"unmapped",w.material.color.copy(xo(N,D,n.METRIC)),w.material.opacity=w.state==="aggregate"?.82:.72});var v=n.$("zlegend");if(v){var S=n.MRANGE[n.METRIC];v.innerHTML="<span>"+S[0]+" "+S[2]+'</span><i style="background:linear-gradient(90deg,'+Ls.join(",")+')"></i><span>'+S[1]+" "+S[2]+"</span>"}}};var Rg=n.applyFloor;n.applyFloor=function(){Rg(),n.LAYER.zones.visible=n.LAYCHK("zones"),n.VALVE.forEach(function(h){h.v.designReplacement&&(h.g.visible=!1)}),Object.keys(Wn).forEach(function(h){Wn[h].visible=hn(+h)}),Object.keys(Bt).forEach(function(h){Bt[h].visible=hn(+h)&&n.$("officeInstruments").checked}),Object.keys(ri).forEach(function(h){ri[h].visible=hn(+h)&&n.$("officeVAV").checked}),[Bt,ri].forEach(function(h){Object.values(h).forEach(function(_){_.children.forEach(function(v){var S=n.EQ[v.userData.relatedEquipment],w=!S||mi(S)||n.$("showSpare").checked;v.visible=w&&(!v.userData.hardwareTag||n.$("officeDeviceTags").checked)})})})},["officeInstruments","officeVAV","officeDeviceTags"].forEach(function(h){n.$(h).addEventListener("change",n.applyFloor)});var Ep=document.querySelector(".zrow");Ep&&(Ep.style.display="");function fs(h){var _=Ct.find(function(w){return w.id===h});if(_){var v=_.source,S=n.MRANGE[n.METRIC][2];n.$("info").innerHTML="<h3>"+_.id+" \xB7 "+_.room.name+"</h3><table><tr><td>Floor</td><td>"+_.room.floor+"</td></tr><tr><td>Displayed value</td><td>"+(_.value===null?"\u2014":_.value.toFixed(n.METRIC==="t"?1:0)+" "+S)+"</td></tr><tr><td>Data source</td><td>"+(v?v.code+" \xB7 "+v.name:"no mapping")+"</td></tr><tr><td>Point</td><td>"+(v?v[n.METRIC]:"\u2014")+"</td></tr></table><p>"+(v?"Legacy zone aggregate shared by several rooms (no dedicated room sensor)":"New design room: no dedicated room point")+"</p>",n.$("info").className="open"}}n.renderer.domElement.addEventListener("dblclick",function(h){if(n.LAYER.zones.visible){var _=n.renderer.domElement.getBoundingClientRect();n.mp.set((h.clientX-_.left)/_.width*2-1,-(h.clientY-_.top)/_.height*2+1),n.ray.setFromCamera(n.mp,n.camera);var v=n.ray.intersectObjects(Ct.filter(function(w){return Wn[w.room.floor].visible}).map(function(w){return w.mesh}),!1)[0];if(v){var S=n.ray.intersectObjects([...n.LAYER.plant.children,...n.LAYER.air.children],!0).find(function(w){for(var F=w.object;F&&!F.userData.eq;)F=F.parent;return F&&F.visible&&w.distance<v.distance});S||(h.stopImmediatePropagation(),fs(v.object.userData.roomCell))}}},!0),window.__R4={roomCells:Ct,hardwareBounds:ds,openRoom:fs,existingValveBounds:function(){return n.VALVE.filter(function(h){return!h.v.designReplacement}).map(function(h){h.g.updateWorldMatrix(!0,!0);var _=new un().setFromObject(h.g);return{kind:h.v.kind,pipe:h.v.pipe,box:[_.min.x,-_.max.z,_.min.y,_.max.x,-_.min.z,_.max.y]}})},inspect:function(){return{revision:xe.revision,roomCells:Ct.length,mappedCells:Ct.filter(function(h){return!!h.source}).length,visibleCells:Ct.filter(function(h){return n.LAYER.zones.visible&&Wn[h.room.floor].visible}).length,instruments:xe.instruments.length,VAVs:xe.airTerminals.length,zoneLayer:n.LAYER.zones.visible,upperColumnsClipped:Rt[1].structural.children.filter(function(h){return h.isMesh&&h.material.clippingPlanes&&h.material.clippingPlanes.length}).length,visibleDeviceEquipment:Object.values(Bt).filter(function(h){return h.visible}).flatMap(function(h){return h.children.filter(function(_){return _.userData.instrument&&_.visible}).map(function(_){return _.userData.relatedEquipment})}),continuousColumnStacks:xe.columns.length,section:n.$("officeSection").checked}}};var gi={},vo={},ql={},Yl={},Iu=[],$l=!1,Zl=null,Kl=null;xe.roomSensors.forEach(function(h,_){var v=Ct.find(function(D){return D.id===h.cell});v&&(v.source=null,v.sensor=h),gi[h.cell]={t:null,h:null,c:null,o:null,quality:"unbound"};var S=ql[h.floor];S||(S=ql[h.floor]=new Oe,n.LAYER.interiors.add(S));var w=new Oe;S.add(w),w.position.set(h.position[0],h.position[2],-h.position[1]),w.userData.sensor=h.id,Ut(new _t(.115,.135,.04),lt.wall,w,new y),Ut(new cn(.078,.043),nn.screen,w,new y(0,.014,.021)),w.rotation.y=Math.PI/2;var F=n.textSprite("RS",22,"#e4edf1","rgba(18,43,60,.88)");F.position.copy(w.position).add(new y(0,.21,0)),F.scale.set(.56,.28,1),F.userData.hardwareTag=!0,S.add(F),w.updateWorldMatrix(!0,!0);var N=new un().setFromObject(w);Iu.push({id:h.id,kind:"ROOM-SENSOR",floor:h.floor,box:[N.min.x,-N.max.z,N.min.y,N.max.x,-N.min.z,N.max.y]})});function bp(h,_,v){var S=Yl[h.floor];S||(S=Yl[h.floor]=new Oe,n.LAYER.interiors.add(S));var w=new Oe;S.add(w),w.position.set(v[0],v[2],-v[1]),w.userData.meter=_==="PM"?h.powerMeter:h.btuMeter,Ut(new _t(.32,.36,.1),lt.wall,w,new y),Ut(new cn(.23,.095),nn.screen,w,new y(0,.06,.051)),Ut(new _t(.045,.035,.018),nn.actuator,w,new y(.06,-.08,.06));var F=n.textSprite(w.userData.meter,26,"#e4edf1","rgba(18,43,60,.90)");F.position.copy(w.position).add(new y(0,.39,0)),F.scale.set(1.5,.4,1),S.add(F),w.updateWorldMatrix(!0,!0);var N=new un().setFromObject(w);Iu.push({id:w.userData.meter,kind:_,floor:h.floor,box:[N.min.x,-N.max.z,N.min.y,N.max.x,-N.min.z,N.max.y]})}xe.floorMeters.forEach(function(h){bp(h,"PM",h.powerPosition),bp(h,"BTU",h.position)}),Mt.querySelector("h2").textContent="Rental office / Food court \xB7 R5",Mt.querySelectorAll("small").forEach(function(h){h.textContent.includes("aggregate")&&h.remove()}),Mt.insertAdjacentHTML("beforeend",'<label><input id="officeRoomSensors" type="checkbox" checked> Room sensors</label><label><input id="officeFloorMeters" type="checkbox" checked> Floor power / BTU meters</label><label><input id="rentalDemo" type="checkbox" '+(n.DEMO?"checked":"")+'> Simulate sensors / meters (DEMO)</label><small id="rentalSource"></small><div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;font-size:11px"><span style="color:#1559d6">\u25A0 CHWS \u2192 load</span><span style="color:#57c5f5">\u25A0 CHWR \u2192 chiller</span><span style="color:#ed781c">\u25A0 CDR \u2192 tower</span><span style="color:#b29313">\u25A0 CDS \u2192 chiller</span></div><details><summary>Floor meters / billing</summary><div id="floorBillingState"></div><a href="ALT_V79_FloorBilling.html" target="_blank" style="display:block;margin-top:8px">Read meters / calculate billing</a></details>'),Mt.querySelectorAll("label").forEach(function(h){h.style.display="block",h.style.margin="8px 0"}),n.$("rentalSource").style.display="block",n.$("rentalSource").style.lineHeight="1.6",document.querySelector("header h1").textContent="ALT Rental Office \xB7 B1 plant \xB7 R5",document.querySelector("header .sub").textContent="119 suites / 305 dedicated room sensors / 8 floor power + BTU meters";var Cg=n.applyFloor;n.applyFloor=function(){Cg(),[ql,Yl].forEach(function(h,_){Object.keys(h).forEach(function(v){h[v].visible=hn(+v)&&n.$(_?"officeFloorMeters":"officeRoomSensors").checked,h[v].children.forEach(function(S){S.userData.hardwareTag&&(S.visible=n.$("officeDeviceTags").checked)})})})},["officeRoomSensors","officeFloorMeters","rentalDemo"].forEach(function(h){n.$(h).addEventListener("change",function(){n.applyFloor(),Rr()})});function Xn(){return n.$("rentalDemo").checked}function Rr(){var h=Xn(),_=performance.now()/1e3;$l||xe.roomSensors.forEach(function(F,N){var D=0;for(var Y of F.cell)D=D*31+Y.charCodeAt(0)>>>0;var J=D%1e3/83,K=gi[F.cell];K.t=h?23+D%50/10+.25*Math.sin(_/45+J):null,K.h=h?47+D%180/10+Math.sin(_/55+J)*2:null,K.c=h&&F.metrics.includes("CO2_ppm")?450+D%530+20*Math.sin(_/60+J):null,K.o=h&&F.metrics.includes("Occupancy")?D%3!==0:null,K.quality=h?"demo":"unbound"}),Ct.forEach(function(F){var N=gi[F.id],D=N[n.METRIC];F.value=typeof D=="number"&&isFinite(D)?D:null,F.state=N.quality==="demo"?F.value===null?"not-applicable":"dedicated-demo":N.quality,F.material.color.copy(xo(F.value,N.quality!=="demo",n.METRIC)),F.material.opacity=F.state==="dedicated-demo"?.86:.72}),n.$("rentalSource").textContent=h?"DEMO \xB7 every room sensor is independent; floor meters are simulated":"LIVE \xB7 station sensors / meters; grey and \u2014 = no value received",xe.floorMeters.forEach(function(F){var N=F.floor,D=48+N*7,Y=N===1?260:155+N*9,J=D+3*Math.sin(_/45+N),K=Y+4*Math.sin(_/50+N),fe=6.7,te=12.2;vo[N]={quality:h?"demo":"unbound",power_kW:h?J:null,electric_kWh:h?1e4*N+(D*_+135*(Math.cos(N)-Math.cos(_/45+N)))/3600:null,thermal_kW:h?K:null,thermal_kWh:h?2e4*N+(Y*_+200*(Math.cos(N)-Math.cos(_/50+N)))/3600:null,supply_C:h?fe:null,return_C:h?te:null,flow_m3h:h?K/(1.163*(te-fe)):null}});var v=/^\d+$/.test(n.FSEL)?+n.FSEL:2,S=xe.floorMeters.find(function(F){return F.floor===v});if(S){var w=vo[v];n.$("floorBillingState").innerHTML="<p>F"+String(v).padStart(2,"0")+" \xB7 "+S.mode+"</p><p>"+S.powerMeter+" / "+S.btuMeter+"</p><p>"+(h?w.power_kW.toFixed(1)+" kW / "+w.thermal_kW.toFixed(1)+" kW_th<br>"+w.electric_kWh.toFixed(1)+" kWh_e / "+w.thermal_kWh.toFixed(1)+" kWh_th<br>DEMO \xB7 values restart on reload":"\u2014 / LIVE unbound")+"</p><p>Billing uses verified opening / closing readings</p>"}else n.$("floorBillingState").textContent="B1 / roof are common areas outside the rental-floor billing boundary";n.$("info").className==="open"&&(Zl?fs(Zl):Kl&&Pu(Kl))}var Ig=n.updateZones;n.updateZones=function(h){Ig(h),Rr()},fs=function(h){var _=Ct.find(function(w){return w.id===h});if(_){var v=gi[h],S=_.sensor;Zl=h,Kl=null,n.$("info").innerHTML="<h3>"+S.cell+" \xB7 "+S.function+"</h3><table><tr><td>Sensor</td><td>"+S.id+"</td></tr><tr><td>Temperature</td><td>"+(v.t===null?"\u2014":v.t.toFixed(1)+" \xB0C")+"</td></tr><tr><td>RH</td><td>"+(v.h===null?"\u2014":v.h.toFixed(0)+" %")+"</td></tr><tr><td>CO\u2082</td><td>"+(v.c===null?"\u2014":v.c.toFixed(0)+" ppm")+"</td></tr><tr><td>Occupancy</td><td>"+(v.o===null?"\u2014":v.o?"Occupied":"Unoccupied")+"</td></tr></table><p>"+(v.quality==="demo"?"DEMO \xB7 simulated per-room sensor values, not the legacy aggregates":"LIVE \xB7 room sensor points")+"</p><p>installed "+S.height_m+" m AFF \xB7 "+S.function+"</p>",n.$("info").className="open"}};function Pu(h){var _=xe.floorMeters.find(function(N){return N.powerMeter===h||N.btuMeter===h});if(!_)return;Kl=h,Zl=null;var v=vo[_.floor],S=h===_.powerMeter,w=v.quality==="demo";function F(N,D){return v[N]===null?"\u2014":v[N].toFixed(2)+" "+D}n.$("info").innerHTML="<h3>"+h+" \xB7 F"+String(_.floor).padStart(2,"0")+"</h3><table><tr><td>Power</td><td>"+F(S?"power_kW":"thermal_kW",S?"kW":"kW_th")+"</td></tr><tr><td>Energy</td><td>"+F(S?"electric_kWh":"thermal_kWh",S?"kWh_e":"kWh_th")+"</td></tr>"+(S?"":"<tr><td>Flow</td><td>"+F("flow_m3h","m\xB3/h")+"</td></tr><tr><td>TT-S / TT-R</td><td>"+F("supply_C","\xB0C")+" / "+F("return_C","\xB0C")+"</td></tr>")+"</table><p>"+(w?"DEMO \xB7 simulated values restart on reload (display test only)":"LIVE \xB7 floor meter points")+"</p><p>"+_.mode+' \xB7 includes the floor AHU / electrical</p><a href="ALT_V79_FloorBilling.html" target="_blank">Open floor billing</a>',n.$("info").className="open"}n.renderer.domElement.addEventListener("click",function(h){var _=n.renderer.domElement.getBoundingClientRect();n.mp.set((h.clientX-_.left)/_.width*2-1,-(h.clientY-_.top)/_.height*2+1),n.ray.setFromCamera(n.mp,n.camera);var v=[...Object.values(ql),...Object.values(Yl)].filter(function(N){return N.visible}),S=n.ray.intersectObjects(v,!0).find(function(N){for(var D=N.object;D&&!D.userData.sensor&&!D.userData.meter;)D=D.parent;return D});if(S){for(var w=S.object;w&&!w.userData.sensor&&!w.userData.meter;)w=w.parent;if(w.userData.meter)Pu(w.userData.meter);else{var F=xe.roomSensors.find(function(N){return N.id===w.userData.sensor});fs(F.cell)}h.stopImmediatePropagation()}},!0),window.__R4.openRoom=function(h){fs(h)};for(var $e in n.PIPE){var Pt=n.PIPE[$e],Lu=xe.pipeColors[Pt.p.svc];if(Lu&&(Pt.mat.color.set(Lu),Pt.oc=Pt.mat.color.clone(),Pt.wm&&Pt.wm.uniforms))for(var je in Pt.wm.uniforms){var We=Pt.wm.uniforms[je];We.value&&We.value.isColor&&We.value.set(Lu)}}window.__R5={roomValues:gi,floorMeterValues:vo,bounds:Iu,setDemo:function(h){n.$("rentalDemo").checked=h,Rr()},freeze:function(h){$l=h},update:Rr,openRoom:fs,openMeter:Pu,inspect:function(){return{revision:xe.revision,sensors:xe.roomSensors.length,roomCells:Ct.length,powerMeters:xe.floorMeters.length,btuMeters:xe.floorMeters.length,demo:Xn(),sensorPointsBound:0,meterPointsBound:0,layouts:[...new Set(vt.filter(h=>h.kind==="office"&&h.floor>1).map(h=>h.function))],colors:xe.pipeColors}}},n.applyFloor(),Rr(),window.__DESIGN.version="OFFICE-B1-R5";for(var B in n.ZONE){var yo=n.ZONE[B];yo.g.visible=!1,yo.sp&&(yo.sp.visible=!1,yo.sp.parent&&yo.sp.parent.remove(yo.sp))}Ls=["#0639b0","#006b96","#087735","#a28100","#b04400","#b00927"],Mt.querySelector("h2").textContent="Two rental companies / Room HVAC \xB7 R7",document.querySelector("header h1").textContent="ALT Rental Office \xB7 Two companies / floor \xB7 R7",document.querySelector("header .sub").textContent="F02\u2013F08 \xB7 Company A left / Company B right \xB7 room sensors / motorized dampers",n.$("labelsOn").checked=!1,n.$("labelsOn").closest("label").style.display="none",Mt.insertAdjacentHTML("beforeend",'<label><input id="roomReadingsR6" type="checkbox" checked> room temperature figures where a grille exists</label><label><input id="roomDampersR6" type="checkbox" checked> Motorized duct damper</label><small>R7 \xB7 blue 21 \xB0C \u2192 green 24 \xB0C \u2192 red 29 \xB0C<br>Select a floor for room figures \xB7 click a room colour for CFM / grilles<br>DEMO per room \xB7 LIVE from the station points (r6 adapter)</small><a href="ALT_V79_RentalFloor.html" target="_blank" style="display:block;margin-top:8px">2D plan / CFM / damper per room</a>');var _i=[],jl={},Cr=[],Tp=[];Ct.forEach(function(h){if(h.room.numericLabel){var _=document.createElement("canvas");_.width=384,_.height=150;var v=new ci(_);v.colorSpace=sn;var S=new es(new Li({map:v,transparent:!0,depthTest:!1,toneMapped:!1}));S.position.set((h.rect[0]+h.rect[2])/2,$(h.room.floor)+2,-(h.rect[1]+h.rect[3])/2),S.scale.set(3.3,1.29,1),S.renderOrder=30,S.userData.roomCell=h.id,Wn[h.room.floor].add(S),_i.push({cell:h,canvas:_,tex:v,sp:S,last:""})}}),(xe.motorizedDampers||[]).forEach(function(h){var _=jl[h.floor];_||(_=jl[h.floor]=new Oe,n.LAYER.ducts.add(_));var v=new Oe;_.add(v),v.position.set(h.position[0],h.position[2],-h.position[1]),v.rotation.y=h.direction[0]?0:Math.PI/2,v.userData.damper=h.id;var S=h.w,w=h.h;Ut(new _t(.12,w+.035,S+.035),lt.frame,v,new y);var F=Ut(new _t(.022,w*.88,S*.88),lt.metal,v,new y);h.integralVAV||Ut(new _t(.12,.12,.1),nn.actuator,v,new y(0,w/2+.1,0)),v.children[0].material=new ge({color:"#4f6570",wireframe:!0,roughness:.7}),Cr.push({d:h,g:v,blade:F,phase:Cr.length*.71}),v.updateWorldMatrix(!0,!0);var N=new un().setFromObject(v);Tp.push({id:h.id,kind:"MOTORIZED-DAMPER",floor:h.floor,box:[N.min.x,-N.max.z,N.min.y,N.max.x,-N.min.z,N.max.y]})});var Pg=n.applyFloor;n.applyFloor=function(){Pg(),_i.forEach(function(_){_.sp.visible=n.$("roomReadingsR6").checked&&hn(_.cell.room.floor)&&n.ISO&&n.LAYER.zones.visible}),Object.keys(jl).forEach(function(_){jl[_].visible=hn(+_)&&n.$("roomDampersR6").checked&&n.LAYER.ducts.visible});for(var h in n.ZONE)n.ZONE[h].g.visible=!1,n.ZONE[h].sp&&(n.ZONE[h].sp.visible=!1)},["roomReadingsR6","roomDampersR6"].forEach(function(h){n.$(h).addEventListener("change",n.applyFloor)});function Jl(){$l||xe.roomSensors.forEach(function(_){var v=0;for(var S of _.cell)v=v*31+S.charCodeAt(0)>>>0;var w=gi[_.cell];w.t=Xn()?21.7+v%70/10+.2*Math.sin(Date.now()/45e3+v%1e3/83):null});for(var h in n.ZONE)n.ZONE[h].g.visible=!1,n.ZONE[h].sp&&(n.ZONE[h].sp.visible=!1);Ct.forEach(function(_){_.value=gi[_.id][n.METRIC],_.material.color.copy(xo(_.value,!Xn(),n.METRIC)),_.material.opacity=_.state==="dedicated-demo"?.97:.8}),Cr.forEach(function(_){var v=Xn();_.blade.rotation.z=v?(.25+.6*(.5+.5*Math.sin(performance.now()/6e3+_.phase)))*Math.PI/2:0,_.blade.material.color.set(v?"#8da9ad":"#65717b"),_.g.userData.quality=v?"DEMO":"Unbound"})}var Lg=n.updateZones;n.updateZones=function(h){Lg(h),Jl()};var Dg=fs;fs=function(h){Dg(h);var _=Ct.find(function(S){return S.id===h});if(_){var v=_.room;n.$("info").insertAdjacentHTML("beforeend","<table><tr><td>Tenant</td><td>"+(v.tenant||"COMMON")+"</td></tr><tr><td>Area</td><td>"+v.area_m2+" m\xB2</td></tr><tr><td>Supply design</td><td>"+(v.supply_CFM?v.supply_CFM.toFixed(0)+" CFM":"\u2014")+"</td></tr><tr><td>Supply outlets</td><td>"+(v.diffuserCount||0)+"</td></tr><tr><td>OA concept</td><td>"+(v.OA_target_Ls||"\u2014")+" L/s</td></tr></table><p>Airflow / size are concept values from the load allowance; confirm load, NC, throw, ESP and TAB</p>")}},window.__R6={inspect:function(){return{revision:xe.revision,rooms:vt.length,sensors:xe.roomSensors.length,tenancies:xe.tenancies.length,diffusers:xe.diffusers.length,dampers:Cr.length,labels:_i.length,visibleLabels:_i.filter(function(h){return h.sp.visible}).length,oldLabels:Object.values(n.ZONE).filter(function(h){return h.sp&&h.sp.visible}).length,opacity:Ct.map(function(h){return h.material.opacity}),ordinaryStairs:xe.verticalTransport.ordinaryStairs}},labels:_i,damperMeshes:Cr,bounds:Tp,openRoom:fs,refresh:function(){Rr(),Jl(),n.applyFloor()}},Jl(),n.applyFloor(),Mt.querySelector("h2").textContent="Equal companies / AHU all-air \xB7 R7",document.querySelector("header h1").textContent="ALT Rental Office \xB7 Equal companies / AHU VAV \xB7 R7",document.querySelector("header .sub").textContent="F02\u2013F08 \xB7 A / B 888.69 m\xB2 each \xB7 identical room functions \xB7 no FCU",n.$("roomReadingsR6").parentElement.lastChild.textContent=" Room labels \xB7 \xB0C / RH / CO\u2082",Mt.insertAdjacentHTML("beforeend",'<label><input id="airflowR7" type="checkbox" checked> Show airflow by damper feedback</label><label>DEMO room <select id="r7Room"></select></label><div style="display:flex;gap:6px"><button id="r7Open">Open room</button><button id="r7Close">Close room</button></div><small id="r7AirState"></small><a href="ALT_V79_AHU_AllAir.html" target="_blank">AHU / OA\u2013RA\u2013SA\u2013EA / VSD / PICV</a>'),Mt.querySelectorAll("label").forEach(function(h){h.style.display="block"});var Ql={};[].forEach(function(h){var _=Ql[h.floor];_||(_=Ql[h.floor]=new Oe,n.LAYER.air.add(_));var v=new y(h.position[0],h.position[2],-h.position[1]);if(h.kind==="VSD"){Ut(new _t(.42,.7,.24),lt.wall,_,v),Ut(new cn(.2,.1),nn.screen,_,v.clone().add(new y(0,.14,.121)));for(var S of[-.16,-.24])Ut(new _t(.24,.02,.015),lt.frame,_,v.clone().add(new y(0,S,.13)))}else h.kind==="AirMD"?(Ut(new _t(.28,.22,.26),nn.flange,_,v),Ut(new _t(.16,.12,.12),new ln({color:"#ca8c44",roughness:.55}),_,v.clone().add(new y(.2,.05,0))),Ut(new _t(.025,.16,.2),nn.body,_,v)):(Ut(new _t(.075,.065,.07),nn.body,_,v.clone().add(new y(0,.1,0))),Ut(n.cyl(.009,.16,8),nn.flange,_,v.clone()))});var Mo={},ec={},Eo=[],Ir={};xe.rooms.filter(h=>h.supply_CFM).forEach(h=>{n.$("r7Room").add(new Option(h.id+" \xB7 "+h.name,h.id))});function Ri(h){if(Xn()){var _=xe.rooms.find(N=>N.id===h),v=!!ec[h],S=_?_.supply_CFM||(_.exhaust_Ls_concept||0)*2.11888:0,w=_&&_.minimumSA_CFM_concept||0,F=_&&_.supply_CFM?Math.round(100*Math.min(1,Math.max(.65,S?w/S:0))):100;return{quality:"demo",position_pct:v?0:F,airflow_cfm:v?0:Math.min(S,Math.max(S*F/100,w))}}return Mo[h]||{quality:"unbound",position_pct:null,airflow_cfm:null}}function wa(h){var _=Ri(h);return(_.quality==="good"||_.quality==="demo")&&Number.isFinite(_.position_pct)&&Number.isFinite(_.airflow_cfm)&&_.position_pct>5&&_.position_pct<=100&&_.airflow_cfm>1}xe.ducts.filter(h=>h.floor<9&&h.service==="SA"&&!h.id.startsWith("BR-")).forEach(function(h){var _=Ir[h.floor];_||(_=Ir[h.floor]=new Oe,n.LAYER.ducts.add(_));for(var v=[],S=0,w=1;w<h.points.length;w++){var F=Math.hypot(...h.points[w].map((Y,J)=>Y-h.points[w-1][J]));v.push(F),S+=F}if(S){for(var N=[],w=0;w<2;w++){var D=n.mesh(new _t(.18,.065,.065),new ln({color:"#59d6ff",transparent:!0,opacity:.94,depthTest:!1,toneMapped:!1}),_);D.renderOrder=24,N.push(D)}Eo.push({d:h,lengths:v,total:S,glyphs:N})}});function Pr(){$l||xe.roomSensors.forEach(function(w){var F=0;for(var N of w.cell)F=F*31+N.charCodeAt(0)>>>0;var D=gi[w.cell];D.h=Xn()?47+F%180/10+2*Math.sin(Date.now()/55e3+F%1e3/83):null,D.c=Xn()?450+F%530+20*Math.sin(Date.now()/6e4+F%1e3/83):null});var h=0,_=0;xe.rooms.filter(w=>w.supply_CFM).forEach(w=>{wa(w.id)&&h++,Ri(w.id).quality==="unbound"&&_++}),Cr.forEach(function(w){var F=Ri(w.d.room),N=F.quality==="demo"||F.quality==="good",D=N?F.position_pct:0;w.blade.rotation.z=D/100*Math.PI/2,w.g.userData.quality=N?F.quality.toUpperCase():"Unbound",w.g.userData.feedback_pct=N?D:null,w.blade.material.color.set(N?D>5?"#32b58c":"#c5734c":"#65717b")});var v=performance.now()/1e3;Eo.forEach(function(w){var F=w.d.servedRooms||(w.d.room?[w.d.room]:xe.rooms.filter(D=>D.floor===w.d.floor&&D.supply_CFM).map(D=>D.id)),N=F.some(wa)&&n.$("airflowR7").checked&&n.LAYER.ducts.visible&&hn(w.d.floor);w.glyphs.forEach(function(D,Y){if(D.visible=N,!!N){for(var J=(v*1.2+Y*w.total/2)%w.total,K=0;K<w.lengths.length-1&&J>w.lengths[K];)J-=w.lengths[K],K++;var fe=w.d.points[K],te=w.d.points[K+1],pe=J/w.lengths[K];D.position.set(fe[0]+(te[0]-fe[0])*pe,fe[2]+(te[2]-fe[2])*pe,-fe[1]-(te[1]-fe[1])*pe),D.quaternion.setFromUnitVectors(new y(1,0,0),new y(te[0]-fe[0],te[2]-fe[2],fe[1]-te[1]).normalize())}})});for(var S in Rt)Rt[S].ducts.traverse(function(w){w.isMesh&&w.userData.designKind==="duct"&&(w.material.transparent=n.$("airflowR7").checked,w.material.opacity=n.$("airflowR7").checked?.58:1,w.material.depthWrite=!n.$("airflowR7").checked)});window.__R9&&Ua(),n.$("r7AirState").textContent=(Xn()?"DEMO feedback":"LIVE / proposed points")+" \xB7 active "+h+" \xB7 unbound "+_+" \xB7 position + airflow proof"}var Ng=n.updateZones;n.updateZones=function(h){Ng(h),Pr()};var Ug=n.applyFloor;n.applyFloor=function(){Ug(),Object.keys(Ql).forEach(h=>Ql[h].visible=hn(+h)&&n.LAYER.air.visible),Object.keys(Ir).forEach(h=>Ir[h].visible=hn(+h)&&n.$("airflowR7").checked&&n.LAYER.ducts.visible)},n.$("airflowR7").onchange=()=>{n.applyFloor(),Pr()};function Sp(h){if(!Xn()){n.$("r7AirState").textContent="Turn on DEMO to try; this button never writes station commands";return}ec[n.$("r7Room").value]=!h,Pr()}n.$("r7Open").onclick=()=>Sp(!0),n.$("r7Close").onclick=()=>Sp(!1),window.__R7={feedback:Mo,demoClosed:ec,paths:Eo,state:Ri,flow:wa,setRoomDemo:function(h,_){ec[h]=!_,Pr()},applyFeedback:function(h,_){if(!xe.rooms.some(v=>v.id===h))throw Error("Unknown room");Mo[h]=_,Pr()},refresh:function(){Rr(),Jl(),Pr(),n.applyFloor()},inspect:function(){return{revision:xe.revision,FCUs:xe.equipment.filter(h=>h.type==="fcu").length+window.MODEL.air_equipment.filter(h=>h.type==="fcu").length,companies:xe.tenancies.map(h=>({id:h.id,gross:h.grossExclusiveArea_m2,net:h.netRoomArea_m2,functions:h.functions})),movingPaths:Eo.filter(h=>h.glyphs.some(_=>_.visible)).length,labels:_i.length,visibleLabels:_i.filter(h=>h.sp.visible).length}}},document.querySelector('[data-layer="air"]').parentElement.lastChild.textContent=" Air side / AHU / VSD / ventilation",n.$("officeTheme").value="day",Sn(),window.__DESIGN.version=xe.revision,Pr(),n.applyFloor(),Eo.forEach(function(h){h.glyphs.forEach(function(_){_.visible=!1,_.parent.remove(_)})}),Eo.length=0,Mt.querySelector("h2").textContent="Rental office / coordinated ceilings \xB7 R8",document.querySelector("header h1").textContent="ALT Rental Office \xB7 Air distribution / EPMS ready \xB7 R8",Mt.insertAdjacentHTML("beforeend",'<div style="display:flex;flex-wrap:wrap;gap:8px;font-size:11px;margin:10px 0"><span style="color:#238565">\u25CF OA / FA</span><span style="color:#168cb5">\u25CF SA</span><span style="color:#8865b8">\u25CF RA</span><span style="color:#c76b47">\u25CF EA / Toilet</span></div><label><input id="ceilingR8" type="checkbox"> Show ceilings / hide to see the plenum</label><a href="ALT_V79_Tenant_Metering.html" target="_blank">Tenant PM / BTU / EPMS interface</a>');var Lr=[],tc=[],Aa={},Dr={},Ra={},Ca={},Fg=window.__SEAT_AUDIT||[],Nr=document.createElement("canvas");Nr.width=128,Nr.height=32;var Ia=Nr.getContext("2d"),Pa=Ia.createRadialGradient(80,16,1,64,16,64);Pa.addColorStop(0,"rgba(255,255,255,1)"),Pa.addColorStop(.3,"rgba(255,255,255,.85)"),Pa.addColorStop(.65,"rgba(255,255,255,.35)"),Pa.addColorStop(1,"rgba(255,255,255,0)"),Ia.fillStyle=Pa,Ia.fillRect(0,0,128,32);for(var La=Ia.createImageData(128,32),Da=0;Da<32;Da++)for(var Na=0;Na<128;Na++){var nc=(Da*128+Na)*4,Og=Math.pow(Math.sin(Math.PI*Na/127),1.4),Bg=Math.pow(Math.sin(Math.PI*Da/31),4),Hg=.72+.28*Math.sin(Na*.11+Da*.25);La.data[nc]=La.data[nc+1]=La.data[nc+2]=255,La.data[nc+3]=Math.round(255*Og*Bg*Hg)}Ia.putImageData(La,0,0);var Du=new ci(Nr);Du.needsUpdate=!0;var Ur=[];function wp(h,_){var v=new Oe;_.userData.r8Bundles=_.userData.r8Bundles||{};var S=_.userData.r8Bundles[h];return S||(S=_.userData.r8Bundles[h]={color:h,group:_,objects:[]},Ur.push(S)),S.objects.push(v),v}function kg(h,_,v){for(var S=[],w=0,F=1;F<_.length;F++){var N=Math.hypot(..._[F].map((K,fe)=>K-_[F-1][fe]));S.push(N),w+=N}if(!(w<.04)){for(var D=Math.min(5,Math.max(1,Math.round(w/4))),Y=[],J=0;J<D;J++)Y.push(wp(xe.airColors[h.service]||"#cccccc",v));Lr.push({d:h,points:_,lengths:S,total:w,glyphs:Y})}}(xe.ductBodies||xe.ducts).forEach(function(h){var _=Ir[h.floor];_||(_=Ir[h.floor]=new Oe,n.LAYER.ducts.add(_)),kg(h,h.flowDirection==="reverse"?h.points.slice().reverse():h.points,_)}),xe.diffusers.filter(h=>h.service==="SA").forEach(function(h){for(var _=Ir[h.floor],v=0;v<1;v++)tc.push({t:h,index:v,o:wp(xe.airColors[h.service],_)})}),Ur.forEach(function(h){var _=new _t(1,1,1),v=_.attributes.position.constructor,S=_.attributes.uv.constructor,w=new _t(1,1,1),F=h.objects.length,N=[],D=[];h.positions=new Float32Array(F*24);for(var Y=new Float32Array(F*24),J=0;J<F;J++)for(var K=0;K<2;K++){N.push(0,0,1,0,1,1,0,1);var fe=J*8+K*4;D.push(fe,fe+1,fe+2,fe,fe+2,fe+3);for(var te=0;te<4;te++)Y[(fe+te)*3+2]=1}w.setAttribute("position",new v(h.positions,3)),h.positions=w.attributes.position.array,w.setAttribute("normal",new v(Y,3)),w.setAttribute("uv",new S(new Float32Array(N),2)),w.setIndex(D),w.clearGroups(),h.geometry=w,h.mesh=n.mesh(w,new ln({color:h.color,map:Du,transparent:!0,opacity:.83,depthWrite:!1,side:mn,toneMapped:!1}),h.group),h.mesh.frustumCulled=!1,h.mesh.userData.r8Tracer=!0,_.dispose()});function Vg(){var h=new y,_=[[-.55,-.09,0],[.55,-.09,0],[.55,.09,0],[-.55,.09,0],[-.55,0,-.09],[.55,0,-.09],[.55,0,.09],[-.55,0,.09]];Ur.forEach(function(v){var S=!1;v.objects.forEach(function(w,F){var N=F*24;if(!w.visible){v.positions.fill(0,N,N+24);return}S=!0;for(var D=0;D<8;D++)h.set(_[D][0]*w.scale.x,_[D][1]*w.scale.y,_[D][2]*w.scale.z).applyQuaternion(w.quaternion).add(w.position),v.positions[N+D*3]=h.x,v.positions[N+D*3+1]=h.y,v.positions[N+D*3+2]=h.z}),v.mesh.visible=S,v.geometry.attributes.position.needsUpdate=!0})}function Wi(h){return h&&["good","demo"].includes(h.quality)&&Number.isFinite(h.position_pct)&&h.position_pct>5&&h.position_pct<=100&&Number.isFinite(h.airflow_cfm)&&h.airflow_cfm>1&&(h.quality==="demo"||Number.isFinite(h.timestamp)&&Date.now()-h.timestamp>=0&&Date.now()-h.timestamp<=3e4)}function Ap(h){if(h.room)return Wi(Ri(h.room));var _=h.servedRooms||xe.rooms.filter(v=>v.supply_CFM&&(h.floor===9||v.floor===h.floor)).map(v=>v.id);return["SA","RA"].includes(h.service)?_.some(v=>Wi(Ri(v))):Xn()?h.service==="TE"||h.service==="KE"||h.service==="MA"||h.service==="PA"||h.service==="PE"||_.some(v=>Wi(Ri(v))):Wi(Aa[h.id])}function zg(h,_){for(var v=0;v<h.lengths.length-1&&_>h.lengths[v];)_-=h.lengths[v],v++;var S=h.points[v],w=h.points[v+1],F=_/h.lengths[v],N=Math.min(.12,h.d.h/3,h.d.w/5),D=null,Y=null,J=null;if(v>0&&_<N?(D=S,Y=h.points[v-1],J=w,F=(_+N)/(2*N)):v<h.lengths.length-1&&_>h.lengths[v]-N&&(D=w,Y=S,J=h.points[v+2],F=(_-h.lengths[v]+N)/(2*N)),D){var K=new y(D[0],D[2],-D[1]),fe=new y(D[0]-Y[0],D[2]-Y[2],Y[1]-D[1]).normalize(),te=new y(J[0]-D[0],J[2]-D[2],D[1]-J[1]).normalize(),pe=K.clone().addScaledVector(fe,-N),ze=K.clone().addScaledVector(te,N),Ue=pe.clone().multiplyScalar((1-F)*(1-F)).addScaledVector(K,2*(1-F)*F).addScaledVector(ze,F*F),at=K.clone().sub(pe).multiplyScalar(1-F).addScaledVector(ze.clone().sub(K),F).normalize();return{position:Ue,direction:at}}return{position:new y(S[0]+(w[0]-S[0])*F,S[2]+(w[2]-S[2])*F,-S[1]-(w[1]-S[1])*F),direction:new y(w[0]-S[0],w[2]-S[2],S[1]-w[1]).normalize()}}function Rp(){var h=n.$("airflowR7").checked&&n.LAYER.ducts.visible,_=performance.now()/1e3;Lr.forEach(function(v){var S=h&&hn(v.d.floor)&&Ap(v.d);v.glyphs.forEach(function(w,F){if(w.visible=S,!!S){var N=Math.max(.7,Math.min(2.5,(v.d.velocity_ms||2)*.45)),D=(_*N+F*v.total/v.glyphs.length)%v.total,Y=zg(v,D),J=new y().crossVectors(Y.direction,new y(0,1,0));J.length()<.1&&J.set(1,0,0),J.normalize();var K=new y().crossVectors(J,Y.direction).normalize(),fe=F*2.399+_*.8,te=Math.max(.2,Math.min(.42,Math.min(v.d.w,v.d.h)*1.1));w.position.copy(Y.position),w.quaternion.setFromUnitVectors(new y(1,0,0),Y.direction),w.scale.set(te/1.1,te*.8/.18,te*.8/.18)}})}),tc.forEach(function(v){var S=v.t,w=h&&hn(S.floor)&&n.FSEL!=="all"&&n.FSEL!=="roof"&&Wi(Ri(S.room));if(v.o.visible=w,!!w){var F=(_*.43+v.index/3)%1,N=v.index*Math.PI*2/3,D=S.service==="SA"?F:1-F,Y=.06+D*.34,J=.06+D*.8,K=S.position;v.o.position.set(K[0],K[2]-.1-F*.5,-K[1]),v.o.quaternion.setFromUnitVectors(new y(1,0,0),new y(0,-1,0));var fe=.24*(1-F*.45);v.o.scale.set(fe/1.1,fe*.8/.18,fe*.8/.18)}}),Vg()}xe.corridorSensors.forEach(function(h){var _=Ra[h.floor];_||(_=Ra[h.floor]=new Oe,n.LAYER.air.add(_));var v=new y(h.position[0],h.position[2],-h.position[1]),S=new Oe;_.add(S),S.position.copy(v),S.userData.corridorSensor=h.id,Ut(new _t(.12,.12,.035),lt.wall,S,new y(0,0,0)),Ut(new cn(.075,.035),lt.screen,S,new y(0,.016,.018));var w=document.createElement("canvas");w.width=320,w.height=130;var F=new ci(w),N=new es(new Li({map:F,depthTest:!1,transparent:!0}));N.position.set(0,.55,0),N.scale.set(2.8,1.14,1),S.add(N),Dr[h.id]={s:h,canvas:w,tex:F,unit:S,temperature_C:null,RH_pct:null,CO2_ppm:null,quality:"unbound"}});function Cp(){Object.values(Dr).forEach(function(h){var _=h.s,v=0;for(var S of _.id)v=v*31+S.charCodeAt(0)>>>0;var w=Xn();h.temperature_C=w?23+v%30/10:null,h.RH_pct=w?48+v%100/10:null,h.CO2_ppm=w?480+v%300:null,h.quality=w?"demo":"unbound";var F=[h.quality,h.temperature_C,h.RH_pct,h.CO2_ppm].join("|");if(h.last!==F){h.last=F;var N=h.canvas.getContext("2d");N.fillStyle="rgba(25,41,48,.94)",N.fillRect(0,0,320,130),N.fillStyle="#d8e4e4",N.font="17px Segoe UI",N.fillText(_.id,10,26),N.fillStyle="#fff",N.font="bold 29px Segoe UI",N.fillText(w?h.temperature_C.toFixed(1)+" \xB0C":"\u2014 / unbound",10,65),N.font="18px Segoe UI",N.fillText(w?"RH "+h.RH_pct.toFixed(0)+"% \xB7 CO\u2082 "+h.CO2_ppm+" ppm":"RH \u2014 \xB7 CO\u2082 \u2014",10,98),N.font="12px Segoe UI",N.fillText(w?"DEMO / corridor sensor":"Proposed / no station ORD",10,119),h.tex.needsUpdate=!0}})}xe.rooms.filter(h=>h.floor>=1&&h.floor<=8&&h.kind!=="mechanical").forEach(function(h){var _=h.floor,v=Ca[_];v||(v=Ca[_]=new Oe,n.LAYER.shell.add(v));for(var S=h.rect,w=$(_)+(_===1?3.2:2.7)+.025,F=Ae(v,_,"ceiling",!0),N=xe.diffusers.filter(pe=>pe.room===h.id&&pe.service!=="TA").map(pe=>[pe.position[0]-pe.face_m[0]/2-.025,pe.position[1]-pe.face_m[1]/2-.025,pe.position[0]+pe.face_m[0]/2+.025,pe.position[1]+pe.face_m[1]/2+.025]),D=[S[0],S[2],...N.flatMap(pe=>[Math.max(S[0],pe[0]),Math.min(S[2],pe[2])])].sort((pe,ze)=>pe-ze),Y=[S[1],S[3],...N.flatMap(pe=>[Math.max(S[1],pe[1]),Math.min(S[3],pe[3])])].sort((pe,ze)=>pe-ze),J=1;J<D.length;J++)for(var K=1;K<Y.length;K++){var fe=(D[J]+D[J-1])/2,te=(Y[K]+Y[K-1])/2;N.some(pe=>fe>pe[0]&&fe<pe[2]&&te>pe[1]&&te<pe[3])||F.box("wall",fe,w,te,D[J]-D[J-1],.045,Y[K]-Y[K-1],0,!0)}F.flush()}),xe.tenantMetering.forEach(function(h){var _=Ra[h.floor],v=h.powerPosition;Ut(new _t(.24,.34,.14),nn.body,_,new y(v[0],v[2],-v[1])),Ut(new cn(.16,.08),lt.screen,_,new y(v[0],v[2]+.04,-v[1]+.071))});var Gg=n.updateZones;n.updateZones=function(h){Gg(h),Rp(),Cp()};var Wg=n.applyFloor;n.applyFloor=function(){Wg(),Object.keys(Ra).forEach(h=>Ra[h].visible=hn(+h)&&n.LAYER.air.visible),Object.keys(Ca).forEach(h=>Ca[h].visible=hn(+h)&&n.LAYER.shell.visible&&n.$("ceilingR8").checked)},n.$("ceilingR8").onchange=n.applyFloor;var Xg=window.__R7.applyFeedback;window.__R7.applyFeedback=function(h,_){Xg(h,Object.assign({timestamp:Date.now()},_))},wa=function(h){return Wi(Ri(h))},window.__R7.flow=wa,window.__R8={paths:Lr,jets:tc,sensors:Dr,ceilings:Ca,moving:Ap,valid:Wi,seatAudit:Fg,applyServiceFeedback:function(h,_){if(!xe.ducts.some(v=>v.id===h))throw Error("Unknown duct");Aa[h]=Object.assign({timestamp:Date.now()},_)},refresh:function(){__R7.refresh(),Rp(),Cp(),n.applyFloor()},inspect:function(){return{revision:xe.revision,airServices:[...new Set(Lr.map(h=>h.d.service))],moving:Lr.filter(h=>h.glyphs.some(_=>_.visible)).length,corridorSensors:xe.corridorSensors.length,ceilingVisible:n.$("ceilingR8").checked,tenantMeters:xe.tenantMetering.length}}},__R8.refresh(),Mt.querySelector("h2").textContent="Room HVAC / airflow inspection \xB7 R9",document.querySelector("header h1").textContent="ALT Rental Office \xB7 Coordinated ducts / room conditions \xB7 R9",Mt.insertAdjacentHTML("beforeend",'<label><input id="airXrayR9" type="checkbox" checked> Transparent ducts / airflow inside</label><small>Air colours by service \xB7 labels use the room colour of the selected metric \xB0C / RH / CO\u2082<br>Air tracers show direction and feedback; the speed is not a CFD result</small>');function ic(){var h=n.$("airXrayR9").checked&&n.$("airflowR7").checked;for(var _ in Rt)Rt[_].ducts.traverse(function(v){v.isMesh&&v.userData.designKind==="duct"&&(v.material.transparent=h,v.material.opacity=h?.14:1,v.material.depthWrite=!h,v.renderOrder=h?8:0)});Ur.forEach(function(v){v.mesh.material.depthTest=!h,v.mesh.material.depthWrite=!1,v.mesh.renderOrder=h?21:0})}function Ua(){_i.forEach(function(h){var _=gi[h.cell.id],v=Ri(h.cell.id),S=h.cell.material.color.getHexString(),w=n.METRIC==="h"?"RH":n.METRIC==="c"?"CO\u2082":"TEMP",F=_[n.METRIC],N=n.METRIC==="h"?" %RH":n.METRIC==="c"?" ppm":" \xB0C",D=Xn()?"DEMO":Wi(v)?"Feedback good":"LIVE unbound",Y=[n.METRIC,S,_.t,_.h,_.c,D,v.position_pct].join("|");if(h.r9key!==Y){h.r9key=Y;var J=h.canvas;J.height!==180&&(J.height=180);var K=J.getContext("2d");K.fillStyle="#"+S,K.fillRect(0,0,384,180),K.fillStyle="#ffffff",K.font="600 19px Segoe UI",K.fillText(h.cell.room.name.slice(0,34),12,27),K.font="700 38px Segoe UI",K.fillText(F===null?"\u2014":F.toFixed(n.METRIC==="t"?1:0)+N,12,77),K.font="20px Segoe UI",K.fillText(n.METRIC==="t"?"RH "+(_.h===null?"\u2014":_.h.toFixed(0))+"% \xB7 CO\u2082 "+(_.c===null?"\u2014":_.c.toFixed(0))+" ppm":n.METRIC==="h"?(_.t===null?"\u2014":_.t.toFixed(1))+" \xB0C \xB7 CO\u2082 "+(_.c===null?"\u2014":_.c.toFixed(0))+" ppm":(_.t===null?"\u2014":_.t.toFixed(1))+" \xB0C \xB7 RH "+(_.h===null?"\u2014":_.h.toFixed(0))+"%",12,113),K.font="16px Segoe UI",K.fillText(w+" \xB7 "+D+" \xB7 MD "+(Wi(v)?v.position_pct+"%":"\u2014"),12,155),h.tex.needsUpdate=!0,h.r9color="#"+S,h.r9metric=n.METRIC}}),Object.values(Dr).forEach(function(h){var _=n.METRIC==="h"?h.RH_pct:n.METRIC==="c"?h.CO2_ppm:h.temperature_C,v=xo(_,h.quality!=="demo"&&h.quality!=="good",n.METRIC).getHexString(),S=[n.METRIC,v,h.last].join("|");if(h.r9key!==S){h.r9key=S;var w=h.canvas.getContext("2d");w.fillStyle="#"+v,w.fillRect(0,0,320,130),w.fillStyle="#fff",w.font="16px Segoe UI",w.fillText(h.s.id,10,24),w.font="bold 28px Segoe UI",w.fillText(_===null?"\u2014 / unbound":_.toFixed(n.METRIC==="t"?1:0)+(n.METRIC==="h"?" %RH":n.METRIC==="c"?" ppm":" \xB0C"),10,64),w.font="17px Segoe UI",w.fillText(n.METRIC==="t"?"RH "+(h.RH_pct??"\u2014")+"% \xB7 CO\u2082 "+(h.CO2_ppm??"\u2014")+" ppm":(h.temperature_C===null?"\u2014":h.temperature_C.toFixed(1))+" \xB0C \xB7 "+(n.METRIC==="h"?"CO\u2082 "+(h.CO2_ppm??"\u2014")+" ppm":"RH "+(h.RH_pct??"\u2014")+"%"),10,96),w.font="12px Segoe UI",w.fillText(h.quality==="demo"?"DEMO / corridor sensor":"Proposed / no station ORD",10,119),h.tex.needsUpdate=!0,h.r9color="#"+v}})}var qg=n.updateZones;n.updateZones=function(h){qg(h),ic(),Ua()};var Yg=window.__R8.refresh;window.__R8.refresh=function(){Yg(),ic(),Ua()},n.$("airXrayR9").onchange=window.__R8.refresh,window.__R9={refresh:window.__R8.refresh,paths:Lr,jets:tc,labels:_i,plan:xe,setMetric:function(h){if(!["t","h","c"].includes(h))throw Error("Unknown metric");n.METRIC=h,n.$("zmetric").value=h,window.__R8.refresh()},inspect:function(){return{revision:xe.revision,physicalDuctBodies:xe.ductBodies.length,mergedShells:xe.ductShells.length,moving:Lr.filter(h=>h.glyphs.some(_=>_.visible)).length,metric:n.METRIC,inspection:n.$("airXrayR9").checked}}},window.__R8.refresh(),window.__R9.viewClose=function(h){Nt(String(h)),n.flyTo([31,$(h)+18,11],[17,$(h)+2.7,-12])},window.__R9.bundles=Ur,window.__R9.renderNow=function(){n.renderer.render(n.scene,n.camera)},window.__OFFICE={plan:xe,boxes:X,omitted:xn,focus:Nt,inspect:function(){return{revision:xe.revision,floor:n.FSEL,isolation:n.ISO,theme:n.$("officeTheme").value,visibleFloors:Object.keys(Rt).filter(function(h){return Rt[h].structural.visible}),tenantSuites:vt.filter(function(h){return h.kind==="office"&&h.floor>1}).length,rooms:vt.length,proposedEquipment:xe.equipment.length,render:n.renderer.info.render}}},(function(){var h=Nr.getContext("2d"),_=Nr.width,v=Nr.height;h.clearRect(0,0,_,v);var S=function(w,F){return[w*_,F*v]};h.shadowColor="rgba(255,255,255,.9)",h.shadowBlur=4,h.fillStyle="#ffffff",h.beginPath(),[[.16,.1],[.44,.1],[.84,.5],[.44,.9],[.16,.9],[.56,.5]].forEach(function(w,F){var N=S(w[0],w[1]);F?h.lineTo(N[0],N[1]):h.moveTo(N[0],N[1])}),h.closePath(),h.fill(),Du.needsUpdate=!0,Ur.forEach(function(w){w.mesh.material.opacity=.92,w.mesh.material.depthTest=!0})})();var $g=ic;ic=function(){$g(),Ur.forEach(function(h){h.mesh.material.depthTest=!0,h.mesh.renderOrder=9})};function Zg(h){var _={};return h.getHSL(_),new ke().setHSL(_.h,Math.max(.55,_.s),Math.min(.4,_.l))}function Ip(h,_,v,S,w,F){h.clearRect(0,0,_,v);var N=14;h.fillStyle="rgba(255,255,255,.96)",h.beginPath(),h.moveTo(N,0),h.arcTo(_,0,_,v,N),h.arcTo(_,v,0,v,N),h.arcTo(0,v,0,0,N),h.arcTo(0,0,_,0,N),h.closePath(),h.fill(),h.lineWidth=3,h.strokeStyle="rgba(15,23,42,.28)",h.stroke(),h.save(),h.clip(),h.fillStyle=F?"#94a3b8":"#"+S.getHexString(),h.fillRect(0,0,12,v),h.restore();var D=F?"#64748b":"#"+Zg(S).getHexString(),Y=0;w.forEach(function(J){Y+=J[1],h.font=J[0],h.fillStyle=J[2]==="v"?D:J[2],h.fillText(J[3],24,Y)})}var xi=function(h,_){return h==null||!isFinite(h)?"\u2014":(+h).toFixed(_)};Ua=function(){var h={t:" \xB0C",h:" %RH",c:" ppm"},_={t:1,h:0,c:0};_i.forEach(function(v){var S=gi[v.cell.id],w=Ri(v.cell.id),F=v.cell.material.color,N=S[n.METRIC],D=Xn()?"DEMO":Wi(w)?"LIVE":"LIVE unbound",Y=N==null,J=[n.METRIC,F.getHexString(),S.t,S.h,S.c,D,w.position_pct].join("|");if(v.r9key!==J){v.r9key=J;var K=v.canvas;K.height!==160&&(K.height=160),v.r7scaled||(v.sp.scale.set(2.5,1.04,1),v.r7scaled=!0);var fe=n.METRIC==="t"?"RH "+xi(S.h,0)+" % \xB7 CO\u2082 "+xi(S.c,0)+" ppm":n.METRIC==="h"?xi(S.t,1)+" \xB0C \xB7 CO\u2082 "+xi(S.c,0)+" ppm":xi(S.t,1)+" \xB0C \xB7 RH "+xi(S.h,0)+" %";Ip(K.getContext("2d"),384,160,F,[["600 19px Segoe UI",30,"#334155",v.cell.room.name.slice(0,30)],["700 44px Segoe UI",50,"v",Y?"\u2014":xi(N,_[n.METRIC])+h[n.METRIC]],["18px Segoe UI",32,"#334155",fe],["14px Segoe UI",26,"#64748b",D+(Wi(w)?" \xB7 damper "+w.position_pct+" %":"")]],Y),v.tex.needsUpdate=!0,v.r9color="#"+F.getHexString(),v.r9metric=n.METRIC}}),Object.values(Dr).forEach(function(v){var S=n.METRIC==="h"?v.RH_pct:n.METRIC==="c"?v.CO2_ppm:v.temperature_C,w=S==null,F=xo(S,v.quality!=="demo"&&v.quality!=="good",n.METRIC),N=[n.METRIC,F.getHexString(),v.last].join("|");if(v.r9key!==N){v.r9key=N;var D=v.unit.children.find(function(J){return J.isSprite});D&&!v.r7scaled&&(D.scale.set(2.2,.9,1),v.r7scaled=!0,v.sp=D);var Y=n.METRIC==="t"?"RH "+xi(v.RH_pct,0)+" % \xB7 CO\u2082 "+xi(v.CO2_ppm,0)+" ppm":xi(v.temperature_C,1)+" \xB0C \xB7 "+(n.METRIC==="h"?"CO\u2082 "+xi(v.CO2_ppm,0)+" ppm":"RH "+xi(v.RH_pct,0)+" %");Ip(v.canvas.getContext("2d"),320,130,F,[["600 15px Segoe UI",24,"#334155",v.s.id],["700 32px Segoe UI",38,"v",w?"\u2014":xi(S,n.METRIC==="t"?1:0)+h[n.METRIC]],["15px Segoe UI",27,"#334155",Y],["12px Segoe UI",22,"#64748b",v.quality==="demo"?"DEMO \xB7 corridor sensor":v.quality==="good"?"LIVE \xB7 corridor sensor":"LIVE unbound \xB7 corridor sensor"]],w),v.tex.needsUpdate=!0,v.r9color="#"+F.getHexString()}})};var Nu=0,nr=new y,Uu="";function Pp(){var h=performance.now();if(!(h-Nu<180)){Nu=h;var _=n.camera,v=n.renderer.domElement,S=v.clientWidth,w=v.clientHeight,F=w/(2*Math.tan(_.fov*Math.PI/360)),N=[_.position.x,_.position.y,_.position.z].map(function(te){return Math.round(te*20)}).join(",")+"|"+[_.quaternion.x,_.quaternion.y,_.quaternion.z].map(function(te){return Math.round(te*400)}).join(",")+"|"+n.FSEL+"|"+n.ISO+"|"+S+"x"+w+"|"+n.$("roomReadingsR6").checked+"|"+n.LAYER.zones.visible+"|"+n.LAYER.air.visible;if(N!==Uu){Uu=N;var D=function(te){for(var pe=te.parent;pe;pe=pe.parent)if(!pe.visible)return!1;return!0},Y=n.$("roomReadingsR6").checked&&n.ISO&&n.LAYER.zones.visible,J=_i.map(function(te){return{sp:te.sp,ok:Y&&hn(te.cell.room.floor)}}).concat(Object.values(Dr).map(function(te){var pe=te.sp||te.unit.children.find(function(ze){return ze.isSprite});return pe?{sp:pe,ok:!0}:null}).filter(Boolean)),K=[];J.forEach(function(te){var pe=te.sp;if(!te.ok||!D(pe)){pe.visible=!1;return}pe.getWorldPosition(nr);var ze=nr.distanceTo(_.position);if(nr.project(_),nr.z>1||ze>45||Math.abs(nr.x)>1.2||Math.abs(nr.y)>1.2){pe.visible=!1;return}var Ue=pe.scale.x*F/ze,at=pe.scale.y*F/ze;K.push({sp:pe,d:ze,x:(nr.x+1)/2*S,y:(1-nr.y)/2*w,w:Ue,h:at})}),K.forEach(function(te){te.p=te.d-(te.sp.userData.x7On?4:0)}),K.sort(function(te,pe){return te.p-pe.p||te.sp.id-pe.sp.id});var fe=[];K.forEach(function(te){var pe=fe.some(function(ze){return Math.abs(te.x-ze.x)*2<te.w+ze.w+6&&Math.abs(te.y-ze.y)*2<te.h+ze.h+4});te.sp.visible=!pe&&te.h>9,te.sp.userData.x7On=te.sp.visible,te.sp.visible&&fe.push(te)})}}}var Kg=n.updateZones;n.updateZones=function(h){Kg(h),Pp()},window.__R9.declutter=function(){return Nu=0,Uu="",Pp(),{cards:_i.length,shown:_i.filter(function(h){return h.sp.visible}).length}},(function(){var h=function(N){return N.replace(/[^A-Za-z0-9]+/g,"_").replace(/^_|_$/g,"")},_=function(N){return String(N).padStart(2,"0")},v=function(N){var D=n.V[N];return n.FAIL&&n.FAIL.has(N)?null:typeof D=="number"&&isFinite(D)?D:typeof D=="boolean"?D?100:0:null},S=2.11888,w={};(xe.ductBodies||[]).forEach(function(N){if(N.service==="OA")if(N.floor>=2&&N.floor<=8){var D="AHU_F"+_(N.floor);w[N.id]=function(){var Y=v(D+"_OADmpFb"),J=v(D+"_OAFlow");return Y===null||J===null?null:{position_pct:Y,airflow_cfm:J*S}}}else N.floor===9&&(w[N.id]=function(){var Y=v("OAU01_SpeedFeedbackHz"),J=v("OAU01_Airflow");return Y===null||J===null?null:{position_pct:Math.min(100,Y/50*100),airflow_cfm:J*S}})}),n.r9Live=function(){if(!Xn()){var N=Date.now(),D=!n.DEMO&&/^LIVE/.test(n.$("mode").textContent);xe.roomSensors.forEach(function(K){var fe="RM_"+h(K.room),te=gi[K.cell];if(te){te.t=D?v(fe+"_T"):null,te.h=D?v(fe+"_RH"):null,te.c=D?v(fe+"_CO2"):null;var pe=n.V[fe+"_Occ"];te.o=D&&typeof pe=="boolean"?pe:null,te.quality=D&&(te.t!==null||te.h!==null||te.c!==null)?"good":"unbound"}}),Ct.forEach(function(K){var fe=gi[K.id];if(fe){var te=fe[n.METRIC];K.value=typeof te=="number"&&isFinite(te)?te:null,K.state=fe.quality==="good"?K.value===null?"missing":"dedicated-live":"unbound",K.material.color.copy(xo(K.value,fe.quality!=="good",n.METRIC)),K.material.opacity=K.state==="dedicated-live"?.97:.8}}),xe.airTerminals.forEach(function(K){var fe="VAV_"+h(K.room),te=v(fe+"_DmpFb"),pe=v(fe+"_Airflow");D&&te!==null&&pe!==null?Mo[K.room]={quality:"good",position_pct:te,airflow_cfm:pe*S,timestamp:N}:delete Mo[K.room]});for(var Y in w){var J=D?w[Y]():null;J?Aa[Y]=Object.assign({quality:"good",timestamp:N},J):delete Aa[Y]}xe.floorMeters.forEach(function(K){var fe="F"+_(K.floor),te={quality:"unbound"};D&&(te={power_kW:v("PM_"+fe+"_kW"),electric_kWh:v("PM_"+fe+"_kWh"),thermal_kW:v("BTU_"+fe+"_kW"),thermal_kWh:v("BTU_"+fe+"_kWh"),supply_C:v("TT_S_"+fe),return_C:v("TT_R_"+fe),flow_m3h:v("FM_"+fe+"_Flow")},te.quality=te.power_kW!==null||te.thermal_kW!==null?"good":"unbound"),vo[K.floor]=Object.assign(vo[K.floor]||{},te)}),Object.values(Dr).forEach(function(K){var fe="CS_"+h(K.s.id.replace(/^CS-/,""));K.temperature_C=D?v(fe+"_T"):null,K.RH_pct=D?v(fe+"_RH"):null,K.CO2_ppm=D?v(fe+"_CO2"):null,K.quality=D&&K.temperature_C!==null?"good":"unbound",K.last=[K.quality,K.temperature_C,K.RH_pct,K.CO2_ppm].join("|")})}};var F=n.updateZones;n.updateZones=function(N){F(N),Xn()||(n.r9Live(),Cr.forEach(function(D){var Y=Ri(D.d.room),J=Y.quality==="good",K=J?Y.position_pct:0;D.blade.rotation.z=K/100*Math.PI/2,D.blade.material.color.set(J?K>5?"#32b58c":"#c5734c":"#65717b")}),Ua())},window.__R9.live=function(){return{rooms:Object.values(gi).filter(function(N){return N.quality==="good"}).length,terminals:Object.keys(Mo).length,services:Object.keys(Aa).length}}})(),window.__DESIGN.version="OFFICE-B1-R5",Nt("all")})()}var Ul=([n,e,t])=>new y(n,t,-e);var $0={TT:"dev_tt",PT:"dev_pt",MBFV:"dev_mbfv",FM:"dev_fm",BTU:"dev_btu",PICV:"dev_picv",MD:"dev_md",VSD:"dev_vsd",AirTT:"dev_airtt",AirDP:"dev_airdp",AirFlow:"dev_afms",AirMD:"dev_md"},y1={dev_mbfv:.1,dev_picv:.035,dev_fm:.1},Z0={TT:"Temperature transmitter",PT:"Pressure transmitter",FM:"Flow meter (electromagnetic)",BTU:"BTU / energy meter",MBFV:"Motorised butterfly valve",PICV:"Pressure-independent control valve",MD:"Motorised damper",VSD:"Variable speed drive",AirTT:"Duct temperature sensor",AirDP:"Differential pressure transmitter",AirFlow:"Airflow measuring station",AirMD:"AHU damper + actuator",fan:"Roof fan (R9 design)",ahu:"Make-up air unit (R9 design)"};function K0(n,e,t,i){let s=n.clone();s.lengthSq()<1e-9&&s.set(1,0,0),s.normalize();let r,o;if(i&&(r=Ul(i),r.addScaledVector(s,-r.dot(s))),i&&r.lengthSq()>1e-6)r.normalize(),o=new y().crossVectors(s,r).normalize();else{let c=Math.abs(s.y)>.9?new y(Math.abs(s.x)>.9?0:1,0,Math.abs(s.x)>.9?1:0):new y(0,1,0);o=new y().crossVectors(s,c).normalize(),r=new y().crossVectors(o,s).normalize()}let a=new rt().makeBasis(s,r,o);return e&&a.multiply(new rt().makeTranslation(0,e,0)),a.multiply(new rt().makeScale(...Array.isArray(t)?t:[t,t,t]))}function j0(n){let{scene:e,LAYER:t,onFloor:i,V:s,FAIL:r,glb:o,isDemo:a,reapply:c}=n,l=window.OFFICE,u=window.R9BIND||{};if(!l)return null;let d={devices:new Oe};for(let V in d)e.add(d[V]),t[V]=d[V];let f={0:-6,9:34.9};for(let V of l.roomSensors||[])f[V.floor]=V.position[2]-V.height_m;let p=V=>f[V+1]??f[V]+4.2,x=[],b=new Set((l.motorizedDampers||[]).filter(V=>V.integralVAV).map(V=>V.id));for(let V of l.instruments||[]){let Q=$0[V.kind],le=V.radius||.05,Ee=y1[Q],be=Ee?Math.max(.35,Math.min(3,le/Ee)):1,ut=Ee?0:le+(V.insulation||0)-.1;x.push({d:V,kind:V.kind,f:V.floor,mdl:Q,pos:Ul(V.position),m:K0(Ul(V.direction||[1,0,0]),ut,be,V.stem),lamp:.18+le*1.6+(Ee?0:V.insulation||0)})}for(let V of l.ahuAirDevices||[]){let Q=$0[V.kind];x.push({d:V,kind:V.kind,f:V.floor,mdl:Q,pos:Ul(V.position),m:K0(new y(1,0,0),0,V.kind==="AirMD"?[1,.55,.7]:1),lamp:.45})}for(let V of x){let Q=u[V.d.id];V.p=Q?Q.p:null,V.s=Q?Q.s:null}let g={};x.forEach((V,Q)=>{V.i=Q,(g[V.mdl]=g[V.mdl]||[]).push(V)});let m=[];for(let V in g)o(V,Q=>{Q.updateMatrixWorld(!0);let le=[];Q.traverse(be=>{be.isMesh&&le.push({g:be.geometry,mat:be.material,mw:be.matrixWorld.clone()})});let Ee={};for(let be of g[V])(Ee[be.f]=Ee[be.f]||[]).push(be);for(let be in Ee){let ut=Ee[be];for(let et of le){let ct=new ii(et.g,et.mat,ut.length);ct.castShadow=!1,ct.receiveShadow=!0,ut.forEach((ae,me)=>ct.setMatrixAt(me,new rt().makeTranslation(ae.pos.x,ae.pos.y,ae.pos.z).multiply(ae.m).multiply(et.mw))),ct.userData.devs=ut,ct.computeBoundingSphere(),d.devices.add(ct),i(+be,ct),m.push(ct)}}c&&c()});let A=[],U=new Ei(.032,10,8),T=new ln({toneMapped:!1}),I={};for(let V of x)(I[V.f]=I[V.f]||[]).push(V);for(let V in I){let Q=I[V],le=new ii(U,T,Q.length);Q.forEach((Ee,be)=>{let ut=new y(0,1,0).applyMatrix4(new rt().extractRotation(Ee.m)).normalize();le.setMatrixAt(be,new rt().makeTranslation(Ee.pos.x+ut.x*Ee.lamp,Ee.pos.y+ut.y*Ee.lamp,Ee.pos.z+ut.z*Ee.lamp)),le.setColorAt(be,new ke(6583435))}),d.devices.add(le),i(+V,le),A.push({im:le,list:Q})}let L=[];for(let V of l.equipment||[]){let Q=new Oe;Q.position.copy(Ul(V.position)),d.devices.add(Q),i(V.floor,Q);let[le,Ee,be]=V.size,ut=V.type==="ahu"?"oau":"roof_fan",et=V.type==="ahu"?[4.2,2,2.2]:[1.2,1.2,1.1];Q.userData.unit=V,L.push({u:V,g:Q,spin:null}),o(ut,ct=>{let ae=ct.clone(!0);ae.scale.set(le/et[0],be/et[2],Ee/et[1]),Q.add(ae);let me=ae.getObjectByName("fanWheel");L.find(qe=>qe.g===Q).spin=me,c&&c()})}let P=V=>typeof s[V]=="number"?s[V]:typeof s[V]=="boolean"?s[V]?100:0:void 0,M=new ke(2278750),C=new ke(16096779),O=new ke(4674921),H=0;function k(V){return V.p?r&&r.has(V.p)?"fail":a()||s[V.p]!==void 0?"ok":"fail":"none"}function q(V,Q,le){if(performance.now()-H>900){H=performance.now();for(let be of A)be.list.forEach((ut,et)=>{let ct=k(ut);be.im.setColorAt(et,ct==="ok"?M:ct==="fail"?C:O)}),be.im.instanceColor.needsUpdate=!0}let Ee=le.flow;d.devices.visible=!document.getElementById("officeInstruments")||document.getElementById("officeInstruments").checked;for(let be of L)be.spin&&(be.spin.rotation.y+=Q*(a()?6:0))}function z(V){let Q=V.intersectObjects(m.filter(be=>be.visible&&be.parent.visible),!1)[0];if(Q&&Q.instanceId!==void 0)return{r:Q.object.userData.devs[Q.instanceId]};let le=V.intersectObjects(L.map(be=>be.g).filter(be=>be.visible),!0)[0];if(!le)return null;let Ee=le.object;for(;Ee&&!Ee.userData.unit;)Ee=Ee.parent;return Ee?{u:Ee.userData.unit}:null}function ee(V){let Q=et=>et===void 0?"\u2014":typeof et=="number"?et.toFixed(2):String(et);if(V.u){let et=V.u;return`<h3>${et.id}</h3><table><tr><td>Type</td><td>${Z0[et.type]||et.type}</td></tr><tr><td>Floor</td><td>${et.floor===9?"Roof":et.floor}</td></tr>
      <tr><td>Size (m)</td><td>${et.size.join(" \xD7 ")}</td></tr><tr><td>Station point</td><td class="no">none (R9 design unit only)</td></tr><tr><td>Design status</td><td>${et.status||"Proposed / unbound"}</td></tr></table>`}let le=V.r,Ee=le.d,be=k(le),ut=[["Type",Z0[le.kind]||le.kind],["Floor",Ee.floor===0?"B1":Ee.floor===9?"Roof":Ee.floor],["Equipment / pipe",[Ee.equipment,Ee.pipe,Ee.room].filter(Boolean).join(" \xB7 ")||"\u2014"],["Station point",le.p?`${le.p}<br><span class="hint">${le.s}</span>`:'<span class="no">none \u2014 see docs/R9_POINT_COVERAGE.csv</span>'],["Value",le.p?`<b class="${be==="ok"?"ok":"no"}">${Q(s[le.p])}</b>${be==="fail"?" (LIVE: not resolved)":""}`:"\u2014"],["R9 design status",Ee.status||Ee.control||"\u2014"]];return Ee.note&&ut.push(["Note",Ee.note]),`<h3>${Ee.id}</h3><table>${ut.map(([et,ct])=>`<tr><td>${et}</td><td>${ct}</td></tr>`).join("")}</table>`}function he(V){for(let Q of x)Q.p&&s[Q.p]===void 0&&(s[Q.p]=/Temp|SAT|RAT|MAT|LAT|TT_/.test(Q.p)?12+2*Math.sin(V/30+Q.i):40+20*Math.sin(V/40+Q.i))}function ue(V){for(let Q of d.devices.children)Q.userData.floor!==void 0&&(Q.visible=V(Q.userData.floor))}return{update:q,pick:z,info:ee,demo:he,stats:()=>({devices:x.length,bound:x.filter(V=>V.p).length,units:L.length,instanced:m.length}),floorVis:ue,DEV:x}}var Qe=window.MODEL,Is=window.ALARMS,Ma=window.PTS,br=window.EFFECTS;for(let n in Ma)Ma[n][0]!=="/"&&(Ma[n]="/"+Ma[n]+"/"+n);Is.forEach(n=>{n.f!==void 0&&(n.s="/"+n.f+"/"+n.n,delete n.f)});var tt=n=>document.getElementById(n),Me=n=>n/1e3,wt=(n,e,t)=>new y(Me(n),Me(t),-Me(e)),J0=new xl,Hl=tt("view"),Fn=new hu({antialias:!0,powerPreference:"high-performance"});Fn.setPixelRatio(Math.min(2,devicePixelRatio));Fn.shadowMap.enabled=!0;Fn.shadowMap.type=gh;Fn.toneMapping=Ml;Fn.toneMappingExposure=.55;Fn.outputColorSpace=sn;Hl.appendChild(Fn.domElement);var _n=new jo,Kn=new An(42,1,.1,4e3);Kn.position.set(95,70,60);var Gn=new pu(Kn,Fn.domElement);Gn.target.set(30,12,-20);Gn.enableDamping=!0;Gn.maxPolarAngle=Math.PI*.495;Gn.minDistance=2;Gn.maxDistance=420;Object.assign(Gn,{zoomToCursor:!0,screenSpacePanning:!0,dampingFactor:.09,zoomSpeed:1.3,panSpeed:1.1,rotateSpeed:.7,keyPanSpeed:25});Gn.mouseButtons={LEFT:Ni.ROTATE,MIDDLE:Ni.DOLLY,RIGHT:Ni.PAN};Gn.touches={ONE:ts.ROTATE,TWO:ts.DOLLY_PAN};Gn.listenToKeyEvents(window);var Ks=null;function Qs(n,e,t=900){Ks={p0:Kn.position.clone(),t0:Gn.target.clone(),p1:new y(...n),t1:new y(...e),s:performance.now(),ms:t}}function M1(){if(!Ks)return;let n=Math.min(1,(performance.now()-Ks.s)/Ks.ms),e=n<.5?2*n*n:1-Math.pow(-2*n+2,2)/2;Kn.position.lerpVectors(Ks.p0,Ks.p1,e),Gn.target.lerpVectors(Ks.t0,Ks.t1,e),n>=1&&(Ks=null)}function Jf(n){let e=Kn.position.clone().sub(Gn.target);Qs(Gn.target.clone().add(e.multiplyScalar(n)).toArray(),Gn.target.toArray(),350)}function cg(){let n=Hl.clientWidth,e=Hl.clientHeight;Fn.setSize(n,e),Kn.aspect=n/e,Kn.updateProjectionMatrix()}addEventListener("resize",cg);cg();var E1=new pa(Fn);_n.environmentIntensity=.3;function Zn(n,e,t,i){let s=document.createElement("canvas");s.width=n,s.height=e;let r=s.getContext("2d");t(r,n,e);let o=new ci(s);return o.colorSpace=sn,o.anisotropy=8,i&&(o.wrapS=o.wrapT=oi,o.repeat.set(...i)),o}function xa(n,e,t,i,s,r){n.fillStyle=i,n.fillRect(0,0,e,t);for(let o=0;o<r;o++){let a=(Math.random()-.5)*s;n.fillStyle=`rgba(${a>0?255:0},${a>0?255:0},${a>0?255:0},${Math.abs(a)})`;let c=Math.random()*3+.5;n.fillRect(Math.random()*e,Math.random()*t,c,c)}}var En={concrete:Zn(512,512,(n,e,t)=>{xa(n,e,t,"#b3ada2",.14,16e3),n.strokeStyle="rgba(0,0,0,.18)",n.lineWidth=2,n.strokeRect(0,0,e,t)},[6,4]),asphalt:Zn(512,512,(n,e,t)=>xa(n,e,t,"#3a3c3f",.25,22e3),[60,60]),grass:Zn(512,512,(n,e,t)=>{xa(n,e,t,"#5d7b36",.22,2e4);for(let i=0;i<9e3;i++){let s=Math.random()*e,r=Math.random()*t,o=90+Math.random()*70|0;n.strokeStyle=`rgba(${o*.55|0},${o},${o*.35|0},.55)`,n.beginPath(),n.moveTo(s,r),n.lineTo(s+Math.random()*2-1,r-3-Math.random()*4),n.stroke()}},[90,90]),roof:Zn(512,512,(n,e,t)=>{xa(n,e,t,"#a9a49a",.12,12e3)},[4,3]),wall:Zn(256,256,(n,e,t)=>xa(n,e,t,"#cfc9be",.08,5e3),[4,2]),louvre:Zn(128,128,(n,e,t)=>{n.fillStyle="#2d3a35",n.fillRect(0,0,e,t);for(let i=0;i<t;i+=8)n.fillStyle="#4b5f57",n.fillRect(0,i,e,4)},[1,1]),ctPanel:Zn(256,256,(n,e,t)=>{xa(n,e,t,"#c8cdd0",.06,3e3);for(let i=0;i<e;i+=32)n.fillStyle="rgba(0,0,0,.10)",n.fillRect(i,0,3,t)},[2,1]),ctLouvre:Zn(128,256,(n,e,t)=>{n.fillStyle="#20302c",n.fillRect(0,0,e,t);for(let i=0;i<t;i+=10){let s=n.createLinearGradient(0,i,0,i+7);s.addColorStop(0,"#5e7a6f"),s.addColorStop(1,"#2b3d37"),n.fillStyle=s,n.fillRect(0,i,e,7)}},[3,3]),facade:Zn(512,256,(n,e,t)=>{n.fillStyle="#e9e6df",n.fillRect(0,0,e,t),n.fillStyle="#c4c9cc";for(let i=0;i<e;i+=64)n.fillRect(i,0,2,t);n.fillStyle="#5d7486",n.fillRect(0,t*.62,e,t*.2),n.fillStyle="rgba(255,255,255,.25)";for(let i=0;i<e;i+=64)n.fillRect(i+4,t*.64,24,t*.16)},[8,1]),water:Zn(256,256,(n,e,t)=>{n.fillStyle="#4f7f8f",n.fillRect(0,0,e,t);for(let i=0;i<300;i++){n.strokeStyle="rgba(255,255,255,.18)",n.beginPath();let s=Math.random()*e,r=Math.random()*t;n.moveTo(s,r),n.lineTo(s+18,r+2),n.stroke()}},[1,1]),fall:Zn(64,256,(n,e,t)=>{let i=n.createLinearGradient(0,0,0,t);i.addColorStop(0,"rgba(190,225,240,.0)"),i.addColorStop(.1,"rgba(190,225,240,.75)"),i.addColorStop(1,"rgba(150,200,220,.35)"),n.fillStyle=i,n.fillRect(0,0,e,t);for(let s=0;s<60;s++)n.fillStyle="rgba(255,255,255,.55)",n.fillRect(Math.random()*e,Math.random()*t,1.5,14)},[3,1]),soft:Zn(128,128,(n,e,t)=>{let i=n.createRadialGradient(64,64,0,64,64,64);i.addColorStop(0,"rgba(255,255,255,1)"),i.addColorStop(1,"rgba(255,255,255,0)"),n.fillStyle=i,n.fillRect(0,0,e,t)}),cloud:Zn(256,128,(n,e,t)=>{for(let i=0;i<26;i++){let s=40+Math.random()*176,r=50+Math.random()*40,o=18+Math.random()*30,a=n.createRadialGradient(s,r,0,s,r,o);a.addColorStop(0,"rgba(255,255,255,.55)"),a.addColorStop(1,"rgba(255,255,255,0)"),n.fillStyle=a,n.fillRect(0,0,e,t)}})},_e={concrete:new ge({map:En.concrete,roughness:.92}),slab:new ge({map:En.roof,roughness:.9}),wall:new ge({map:En.wall,roughness:.85}),steel:new ge({color:3883077,metalness:.55,roughness:.5}),galv:new ge({color:10791856,metalness:.75,roughness:.38}),almond:new ge({color:14208950,metalness:.25,roughness:.42}),almondDark:new ge({color:12168851,metalness:.3,roughness:.5}),panel:new ge({color:13620180,metalness:.35,roughness:.4}),black:new ge({color:1908772,metalness:.3,roughness:.6}),motor:new ge({color:2969468,metalness:.45,roughness:.45}),iron:new ge({color:4869973,metalness:.6,roughness:.55}),red:new ge({color:11740702,metalness:.3,roughness:.45}),yellow:new ge({color:15774499,metalness:.2,roughness:.5}),ctPanel:new ge({map:En.ctPanel,roughness:.55,metalness:.1}),ctLouvre:new ge({map:En.ctLouvre,roughness:.7}),glassDark:new ge({color:926256,metalness:.9,roughness:.08}),water:new ge({map:En.water,color:9418948,metalness:.2,roughness:.08,transparent:!0,opacity:.85}),frp:new ge({color:15330799,roughness:.42,metalness:.05}),screen:new ge({color:865616,emissive:1732256,emissiveIntensity:.8})};_e.almond.color.set("#dedbd0");_e.almond.roughness=.58;_e.almond.metalness=.12;_e.almondDark.color.set("#a4aaa7");_e.almondDark.roughness=.64;_e.motor.color.set("#345e73");_e.motor.roughness=.52;_e.iron.color.set("#526970");_e.iron.roughness=.65;_e.panel.color.set("#d2d8d7");_e.panel.roughness=.62;_e.panel.metalness=.12;_e.galv.color.set("#a9b2b4");_e.galv.roughness=.48;_e.galv.metalness=.68;_e.frp.color.set("#e4e6df");_e.frp.roughness=.72;_e.yellow.color.set("#c9ab50");_e.yellow.roughness=.68;_e.steel.color.set("#667279");_e.steel.roughness=.65;var kl={};for(let n in Qe.service){let[,e,t]=Qe.service[n];kl[n]=t?new ge({color:13883612,metalness:.85,roughness:.3}):new ge({color:new ke(e),metalness:.35,roughness:.4}),kl[n+"_band"]=new ge({color:new ke(e),metalness:.2,roughness:.5})}function ne(n,e,t,i,s){let r=new dn(n,e);return r.castShadow=r.receiveShadow=!0,i&&r.position.copy(i),s&&r.rotation.set(...s),t.add(r),r}var Ce=(n,e,t,i=0)=>i?new mu(n,e,t,3,i):new _t(n,e,t),pt=(n,e,t=32)=>new fr(n,n,e,t),Su=new ga;Su.scale.setScalar(2500);_n.add(Su);var er=Su.material.uniforms;er.turbidity.value=6;er.rayleigh.value=1.6;er.mieCoefficient.value=.006;er.mieDirectionalG.value=.85;var wi=new Qr(16773852,3.2);wi.castShadow=!0;wi.shadow.mapSize.set(4096,4096);Object.assign(wi.shadow.camera,{left:-60,right:60,top:60,bottom:-60,near:1,far:400});wi.shadow.bias=-4e-4;wi.shadow.normalBias=.03;_n.add(wi,wi.target);wi.target.position.set(32,0,-20);var bu=new fl(13624319,5919816,.55);_n.add(bu);var hp=ne(new cn(1600,1600),new ge({map:En.grass,roughness:1}),_n,new y(32,-.32,-20),[-Math.PI/2,0,0]),up=ne(new cn(130,100),new ge({map:En.asphalt,roughness:.85,metalness:.05}),_n,new y(32,-.3,-20),[-Math.PI/2,0,0]),b1=[up.material,hp.material,_e.slab];for(let n=0;n<30;n++)ne(Ce(.12,.01,5),new ge({color:15263968,roughness:.8}),_n,new y(-4+n*2.6,-.29,12));var hg=[];for(let n=0;n<7;n++){let e=new Oe;e.position.set(-10+n*14,-.3,22),_n.add(e),ne(pt(.09,9,10),_e.galv,e,new y(0,4.5,0)),ne(Ce(1.2,.18,.4),_e.galv,e,new y(.5,9,0));let t=new Di(16766624,0,40,1.6);t.position.set(.6,8.7,0),e.add(t),hg.push(t)}var ug=pt(.18,3,8),dg=new cl(1.9,1),vw=new ge({color:4025135,roughness:.95,flatShading:!0}),fg=new ge({color:5981746,roughness:1}),dp=[],Qf=[3103268,3894058,4880946,3497772,5669178].map(n=>new ge({color:n,roughness:.9,flatShading:!0}));for(let n=0;n<70;n++){let e=Math.random()*Math.PI*2,t=62+Math.random()*80,i=32+Math.cos(e)*t,s=-20+Math.sin(e)*t,r=new Oe;r.position.set(i,-.3,s);let o=.8+Math.random()*.8;r.scale.setScalar(o),r.rotation.y=Math.random()*6,_n.add(r),ne(ug,fg,r,new y(0,1.5,0));for(let a=0;a<5;a++)ne(dg,Qf[(n+a)%Qf.length],r,new y((Math.random()-.5)*1.8,3.4+Math.random()*1.4,(Math.random()-.5)*1.8)).scale.setScalar(.55+Math.random()*.4);dp.push(r)}var os=new Oe;_n.add(os);{let n=[{x:35,z:40,w:380,d:12},{x:35,z:-85,w:380,d:12},{x:110,z:-22,w:12,d:330},{x:-50,z:-22,w:12,d:330}],e=(P,M,C=0)=>n.some(O=>Math.abs(P-O.x)<O.w/2+C&&Math.abs(M-O.z)<O.d/2+C),t=new ge({map:En.asphalt,color:10132122,roughness:.9}),i=new ge({color:13223355,roughness:.95}),s=new ge({color:14868181,roughness:.8}),r=new ge({color:15921898,roughness:.7}),o=new ge({color:15254068,roughness:.7});for(let P of n){ne(Ce(P.w,.04,P.d),t,os,new y(P.x,-.3,P.z));let M=P.w>P.d,C=M?P.w:P.d;for(let k of[-1,1]){let q=(M?P.d:P.w)/2+1.9;ne(Ce(M?C:3.5,.16,M?3.5:C),i,os,new y(P.x+(M?0:k*q),-.22,P.z+(M?k*q:0))),ne(Ce(M?C:.2,.2,M?.2:C),s,os,new y(P.x+(M?0:k*(q-1.8)),-.2,P.z+(M?k*(q-1.8):0)))}let O=new ii(Ce(M?3:.15,.02,M?.15:3),r,Math.floor(C/8)),H=new rt;for(let k=0;k<O.count;k++){let q=-C/2+4+k*8;H.makeTranslation(P.x+(M?q:0),-.27,P.z+(M?0:q)),O.setMatrixAt(k,H)}os.add(O);for(let k of[-1,1])ne(Ce(M?C:.12,.02,M?.12:C),o,os,new y(P.x+(M?0:k*(P.w/2-.4)),-.27,P.z+(M?k*(P.d/2-.4):0)))}let a=[];for(let P=0;P<28;P++)Math.random()<.7&&a.push([-2.7+P*2.6,12,0]);for(let P of[-27,-19,-11])for(let M=0;M<20;M++){let C=-62+M*2.6;Math.random()<.6&&a.push([P,C,Math.PI/2])}for(let P of[-27,-19,-11])for(let M=0;M<21;M++)ne(Ce(5,.01,.12),r,os,new y(P,-.28,-63.3+M*2.6));let c=[16053490,1908514,9080982,8003362,2046559,12106946,3820090],l=new ii(Ce(1.8,.75,4.4,.12),new ge({roughness:.35,metalness:.55}),a.length),u=new ii(Ce(1.6,.55,2.3,.12),new ge({color:1778736,roughness:.15,metalness:.6}),a.length),d=new ii(pt(.33,.22,14),new ge({color:1118481,roughness:.9}),a.length*4),f=new rt,p=new rn,x=new rn().setFromEuler(new Pi(0,0,Math.PI/2)),b=new y(1,1,1);a.forEach(([P,M,C],O)=>{p.setFromEuler(new Pi(0,C,0)),l.setMatrixAt(O,f.compose(new y(P,.25,M),p,b)),l.setColorAt(O,new ke(c[O*7%c.length])),u.setMatrixAt(O,f.compose(new y(P,.85,M).add(new y(0,0,-.2).applyQuaternion(p)),p,b)),[[-.85,1.35],[.85,1.35],[-.85,-1.35],[.85,-1.35]].forEach(([H,k],q)=>d.setMatrixAt(O*4+q,f.compose(new y(P,.03,M).add(new y(H,0,k).applyQuaternion(p)),p.clone().multiply(x),b)))});for(let P of[l,u,d])P.castShadow=!0,P.receiveShadow=!0,os.add(P);let g=Zn(256,256,(P,M,C)=>{P.fillStyle="#d9d6cf",P.fillRect(0,0,M,C);for(let O=0;O<8;O++)for(let H=0;H<6;H++)P.fillStyle=Math.random()<.25?"#7d8f9f":"#5d6f80",P.fillRect(8+H*41,10+O*31,30,18)});g.wrapS=g.wrapT=oi;let m=[[-12,72,34,22,18],[34,74,30,26,30],[80,70,26,20,12],[150,60,30,34,24],[148,10,26,30,36],[146,-50,30,26,16],[150,-120,34,30,22],[80,-122,40,26,28],[20,-124,36,24,14],[-40,-126,30,30,20],[-92,-60,26,34,26],[-94,6,28,30,12],[-90,66,26,26,18]];for(let[P,M,C,O,H]of m){let k=g.clone();k.needsUpdate=!0,k.repeat.set(Math.max(1,Math.round(C/6)),Math.max(1,Math.round(H/3.6)));let q=new ge({map:k,roughness:.75,color:[16777215,15854560,15133679][Math.abs(P+M)%3]}),z=ne(Ce(C,H,O),q,os,new y(P,H/2-.3,M));z.castShadow=z.receiveShadow=!0,ne(Ce(C+.6,.8,O+.6),_e.concrete,os,new y(P,H+.1,M))}let A=(P,M,C)=>m.some(([O,H,k,q])=>Math.abs(P-O)<k/2+C&&Math.abs(M-H)<q/2+C);for(let P of dp)(e(P.position.x,P.position.z,5)||A(P.position.x,P.position.z,3))&&(P.visible=!1);let U=[],T=[];for(let P of n){let M=P.w>P.d,C=M?P.w:P.d;for(let O of[-1,1])for(let H=-C/2+6;H<C/2-6;H+=10){let k=P.x+(M?H:O*(P.w/2+3)),q=P.z+(M?O*(P.d/2+3):H);n.some(z=>z!==P&&e(k,q,4)&&Math.abs(k-z.x)<z.w/2+4&&Math.abs(q-z.z)<z.d/2+4)||A(k,q,1)||k>-36&&k<100&&q>-72&&q<32||(T.push([k,q]),U.push([k,q]))}}let I=new ii(ug,fg,T.length),L=new ii(dg,Qf[1],U.length);T.forEach(([P,M],C)=>{I.setMatrixAt(C,f.makeTranslation(P,1.2,M)),L.setMatrixAt(C,f.compose(new y(P,4,M),new rn,new y(1.1,1.25,1.1)))}),I.castShadow=L.castShadow=!0,os.add(I,L)}var T1={material:{emissiveIntensity:0}};var Ve=Qe.building,zn=Qe.roof_z,Kt={x:Qe.room.x,y:Qe.room.y,h:Qe.room.h,slab:Ve.slab,wall:Qe.room.wall},S1=Me(Kt.wall),pg=Me(Kt.x),mg=Me(Kt.y),w1=Me(Kt.h),jt={shell:new Oe,plant:new Oe,piping:new Oe,air:new Oe,zones:new Oe,systems:new Oe};for(let n in jt)_n.add(jt[n]);var Tr=jt.plant,Wl=[],Tu={},pi=Qe.equipment.some(n=>n.type==="chiller"&&n.z<-1e3),ao=pi?Math.min(...Qe.equipment.filter(n=>n.z<-1e3).map(n=>n.z))-100:0,ls=n=>n===0?ao:n===1?0:Ve.f1_h+(n-2)*Ve.typ_h;function Vn(n,e){return(Tu[n]=Tu[n]||[]).push(e),e.userData.floor=n,e}var A1=ne(Ce(Me(Ve.x)+2,.3,Me(Ve.y)+2),_e.concrete,jt.shell,wt(Ve.x/2,Ve.y/2,-150));pi&&Vn(1,A1);var R1=pi?ne(Ce(Me(Ve.x),.3,Me(Ve.y)),new ge({map:En.concrete,roughness:.55,metalness:.05,color:12172472}),jt.plant,wt(Ve.x/2,Ve.y/2,ao-150)):ne(Ce(pg,.02,mg),new ge({map:En.concrete,roughness:.55,metalness:.05,color:12172472}),jt.plant,wt(Kt.x/2,Kt.y/2,10));pi&&Vn(0,R1);function vu(n,e,t,i,s,r,o){let a=Math.hypot(t-n,i-e),c=new Oe;c.position.copy(wt(n,e,0)),c.rotation.y=-Math.atan2(i-e,t-n);let l=_e.wall.clone();l.transparent=!0,Wl.push(l);let u=[[0,a,0,s]];for(let d of r||[])u=u.flatMap(([f,p,x,b])=>d.x>=p||d.x+d.w<=f?[[f,p,x,b]]:[[f,d.x,x,b],[d.x+d.w,p,x,b],[d.x,d.x+d.w,x,d.z],[d.x,d.x+d.w,d.z+d.h,b]].filter(g=>g[1]-g[0]>1&&g[3]-g[2]>1));for(let[d,f,p,x]of u)ne(Ce(Me(f-d),Me(x-p),S1),l,c,new y(Me((d+f)/2),Me((p+x)/2),0));for(let d of r||[])d.louvre&&ne(Ce(Me(d.w),Me(d.h),.05),new ge({map:En.louvre,roughness:.7}),c,new y(Me(d.x+d.w/2),Me(d.z+d.h/2),0));return(o||jt.shell).add(c),c}var yu=Kt.h;if(!pi)Vn(1,vu(0,0,Kt.x,0,yu,[{x:2e3,w:3e3,z:0,h:3500},{x:12e3,w:4e3,z:2500,h:1800,louvre:!0},{x:24e3,w:4e3,z:2500,h:1800,louvre:!0}])),Vn(1,vu(Kt.x,0,Kt.x,Kt.y,yu,[{x:4e3,w:2400,z:2600,h:1500,louvre:!0}])),Vn(1,vu(Kt.x,Kt.y,0,Kt.y,yu,[{x:3e4,w:1800,z:0,h:2400}])),Vn(1,vu(0,Kt.y,0,0,yu,[]));else{let n=_e.wall.clone();n.transparent=!0,Wl.push(n);let e=-ao-300,t=new Oe;jt.shell.add(t),Vn(0,t);for(let[i,s,r,o]of[[Ve.x/2,-150,Ve.x+300,300],[Ve.x/2,Ve.y+150,Ve.x+300,300],[-150,Ve.y/2,300,Ve.y],[Ve.x+150,Ve.y/2,300,Ve.y]])ne(Ce(Me(r),Me(e),Me(o)),n,t,wt(i,s,ao+e/2));for(let[i,s]of Qe.grid_x)for(let[r,o]of Qe.grid_y)ne(Ce(.6,Me(e),.6),_e.concrete,t,wt(s,o,ao+e/2));for(let i=6e3;i<Ve.x;i+=9e3)for(let s=4e3;s<Ve.y;s+=8e3){let r=wt(i,s,-500);ne(Ce(1.2,.06,.2),new ge({color:16777215,emissive:16774368,emissiveIntensity:1.2}),t,r)}}var Ol=new ge({color:10336450,metalness:.15,roughness:.04,transparent:!0,opacity:.42,depthWrite:!1,side:mn,envMapIntensity:.65}),C1=new ge({color:4146248,metalness:.6,roughness:.4}),fp=_e.slab.clone();fp.transparent=!0;Wl.push(fp);for(let n=2;n<=Ve.floors+1;n++){let e=n>Ve.floors?zn:ls(n);Vn(n,ne(Ce(Me(Ve.x),Me(Ve.slab),Me(Ve.y)),fp,jt.shell,wt(Ve.x/2,Ve.y/2,e-Ve.slab/2)))}for(let n=1;n<=Ve.floors;n++){let e=ls(n),t=(n===1?Ve.f1_h:Ve.typ_h)-Ve.slab,i=new Oe;jt.shell.add(i),Vn(n,i);for(let[s,r,o,a]of[[0,0,Ve.x,0],[Ve.x,0,Ve.x,Ve.y],[Ve.x,Ve.y,0,Ve.y],[0,Ve.y,0,0]]){if(n===1&&!pi&&r===0&&a===0){ne(Ce(Me(Ve.x-Kt.x),Me(t),.03),Ol,i,wt((Kt.x+Ve.x)/2,0,e+t/2));continue}if(n===1&&!pi&&s===0&&o===0){ne(Ce(.03,Me(t),Me(Ve.y-Kt.y)),Ol,i,wt(0,(Kt.y+Ve.y)/2,e+t/2));continue}let c=Math.hypot(o-s,a-r),l=r===a;ne(Ce(l?Me(c):.03,Me(t),l?.03:Me(c)),Ol,i,wt((s+o)/2,(r+a)/2,e+t/2));for(let u=0;u<=c;u+=2e3){let d=l?Math.min(s,o)+u:s,f=l?r:Math.min(r,a)+u;ne(Ce(.06,Me(t),.06),C1,i,wt(d,f,e+t/2))}ne(Ce(l?Me(c):.3,.7,l?.3:Me(c)),_e.concrete,i,wt((s+o)/2,(r+a)/2,e+t-350))}for(let[s,r]of Qe.grid_x)for(let[o,a]of Qe.grid_y)n===1&&!pi&&r<=Kt.x&&a<=Kt.y||ne(Ce(.6,Me(t),.6),_e.concrete,i,wt(r,a,e+t/2))}var gg=new ge({map:En.concrete,color:14867923,roughness:.9,transparent:!0});Wl.push(gg);ne(Ce(Me(Qe.core.x1-Qe.core.x0),Me(zn+3500),Me(Qe.core.y1-Qe.core.y0)),gg,jt.shell,wt((Qe.core.x0+Qe.core.x1)/2,(Qe.core.y0+Qe.core.y1)/2,(zn+3500)/2));for(let[n,e,t,i]of[[Ve.x/2,0,Ve.x,300],[Ve.x/2,Ve.y,Ve.x,300],[0,Ve.y/2,300,Ve.y],[Ve.x,Ve.y/2,300,Ve.y]])Vn(9,ne(Ce(Me(t),Me(Ve.parapet),Me(i)),_e.concrete,jt.shell,wt(n,e,zn+Ve.parapet/2)));var _g=[];if(!pi)for(let n=4e3;n<Kt.x;n+=8e3)for(let e of[3500,11500]){let t=wt(n,e,Kt.h-400);ne(Ce(1.2,.06,.2),new ge({color:16777215,emissive:16774368,emissiveIntensity:1.2}),Tr,t);let i=new Di(16773596,9,14,1.8);i.position.copy(t).add(new y(0,-.2,0)),Tr.add(i),_g.push(i)}function wu(n,e,t,i){let s=document.createElement("canvas"),r=s.getContext("2d");s.width=256,s.height=128,i&&(r.fillStyle=i,r.beginPath(),r.arc(128,64,54,0,7),r.fill()),r.fillStyle=t,r.font=`600 ${e}px "Segoe UI",sans-serif`,r.textAlign="center",r.textBaseline="middle",r.fillText(n,128,66);let o=new es(new Li({map:new ci(s),depthWrite:!1,transparent:!0}));return o.scale.set(1.2,.6,1),o}for(let[n,e]of Qe.grid_x){let t=wu(n,46,"#1b2a36","rgba(255,255,255,.85)");t.position.copy(wt(e,-2500,0)),t.scale.set(1.6,.8,1),jt.shell.add(t)}for(let[n,e]of Qe.grid_y){let t=wu(n,46,"#1b2a36","rgba(255,255,255,.85)");t.position.copy(wt(-2500,e,0)),t.scale.set(1.6,.8,1),jt.shell.add(t)}var zt={};function ho(n){let e=new Oe;e.position.copy(wt(n.x,n.y,n.z)),e.rotation.y=Zs.degToRad(n.rot||0),(n.layer==="air"?jt.air:Tr).add(e),n.floor!==void 0&&n.floor!==null?Vn(n.floor,e):n.type==="ct"&&Vn(9,e);let t={e:n,g:e,parts:{},spin:[],base:e.position.clone(),mats:new Set};return zt[n.id]=t,e.userData.eq=n.id,t}function fn(n,e){let t=e.clone();return n.mats.add(t),t}function Au(n,e){let t=document.createElement("canvas");t.width=n,t.height=e;let i=new ci(t);return i.colorSpace=sn,{mat:new ln({map:i,toneMapped:!1}),draw(r,o="#06263a",a="#7fe3ff"){let c=t.getContext("2d");c.fillStyle=o,c.fillRect(0,0,n,e),c.fillStyle=a,c.font=`600 ${Math.floor(e/(r.length+.6))}px Consolas,monospace`,r.forEach((l,u)=>c.fillText(l,6,(u+1)*e/(r.length+.3))),i.needsUpdate=!0}}}function Q0(n,e,t){ne(pt(.11,.5,24),e,n,t,[0,0,Math.PI/2]),ne(pt(.19,.03,28),_e.iron,n,t.clone().add(new y(-.25,0,0)),[0,0,Math.PI/2])}function I1(n){let e=ho(n),t=Me(n.L),i=Me(n.W),s=Me(n.H),r=e.g,o=fn(e,_e.almond),a=fn(e,_e.almondDark);ne(Ce(t+.3,.1,i+.3),_e.concrete,r,new y(0,-.05,0)),ne(Ce(t,.18,i*.92),fn(e,_e.steel),r,new y(0,.09,0));for(let p of[-1,1])ne(Ce(.25,.55,i*.8),a,r,new y(p*t*.36,.45,0));for(let p of[-1,1])for(let x of[-.7,.7])ne(Ce(.16,.04,.16),_e.black,r,new y(p*t*.42,.02,x));let c=ne(pt(.36,t*.86,40),o,r,new y(0,.62,-.22),[0,0,Math.PI/2]),l=ne(pt(.42,t*.9,40),o,r,new y(0,1.08,.18),[0,0,Math.PI/2]);e.parts.evap=l,e.parts.cond=c;for(let p of[-1,1])ne(pt(.44,.12,40),a,r,new y(p*t*.455,1.08,.18),[0,0,Math.PI/2]),ne(pt(.38,.12,40),a,r,new y(p*t*.44,.62,-.22),[0,0,Math.PI/2]);for(let p of[.43,-.07])Q0(r,fn(e,_e.steel),new y(-t*.5-.05,1.08,p));for(let p of[-.42,-.02])Q0(r,fn(e,_e.steel),new y(-t*.5-.05,.62,p));let u=ne(Ce(t*.36,.55,.62,.08),o,r,new y(t*.05,1.72,.05));e.parts.comp=u,ne(pt(.26,.5,32),a,r,new y(t*.26,1.72,.05),[0,0,Math.PI/2]);for(let[p,x]of[[-t*.28,-.45],[-t*.1,-.45]])ne(pt(.17,.9,28),o,r,new y(p,1.25,x)),ne(new Ei(.17,24,12,0,Math.PI*2,0,Math.PI/2),o,r,new y(p,1.7,x));ne(new bi(.32,.07,14,32,Math.PI),o,r,new y(-t*.19,1.72,-.45));let d=ne(Ce(.32,1.1,.95,.02),fn(e,_e.panel),r,new y(t*.5+.02,1.25,.25));e.parts.panel=d;let f=Au(256,128);ne(new cn(.3,.16),f.mat,r,new y(t*.5+.185,1.45,.25),[0,Math.PI/2,0]),e.parts.lcd=f,e.parts.beacon=ne(pt(.04,.1,14),new ge({color:1776411,emissive:2278750,emissiveIntensity:0}),r,new y(t*.5+.02,1.86,.6)),e.spin=[]}function P1(n){let e=ho(n),t=e.g,i=Me(n.L);ne(Ce(i+.25,.3,Me(n.W)+.35),fn(e,_e.concrete),t,new y(0,.15,0)),ne(Ce(i,.06,Me(n.W)),fn(e,_e.steel),t,new y(0,.33,0));let s=ne(pt(.21,.62,32),fn(e,_e.motor),t,new y(i*.22,.6,0),[0,0,Math.PI/2]);e.parts.motor=s;for(let c=0;c<12;c++){let l=c/12*Math.PI*2;ne(Ce(.6,.02,.05),fn(e,_e.motor),t,new y(i*.22,.6+Math.sin(l)*.215,Math.cos(l)*.215),[l,0,0])}ne(pt(.13,.04,24),fn(e,_e.motor),t,new y(i*.22+.33,.6,0),[0,0,Math.PI/2]);let r=ne(pt(.12,.05,6),_e.black,t,new y(i*.22+.36,.6,0),[0,0,Math.PI/2]);e.spin.push({m:r,axis:"x"}),ne(Ce(.32,.2,.22),_e.yellow,t,new y(-i*.07,.6,0));let o=ne(pt(.035,.3,12),_e.galv,t,new y(-i*.07,.6,0),[0,0,Math.PI/2]);e.spin.push({m:o,axis:"x"});let a=ne(pt(.3,.22,36),fn(e,_e.iron),t,new y(-i*.3,.62,0),[Math.PI/2,0,0]);e.parts.volute=a,ne(pt(.1,.3,24),fn(e,_e.iron),t,new y(-i*.44,.62,0),[0,0,Math.PI/2]),ne(pt(.09,.32,24),fn(e,_e.iron),t,new y(-i*.3,.95,0));for(let c of[-1,1])ne(Ce(.12,.12,.5),_e.steel,t,new y(c*i*.45,.05,0))}function L1(n){let e=ho(n),t=e.g,i=Me(n.L),s=Me(n.W),r=Me(n.H),o=fn(e,_e.frp),a=_e.galv,c=Me(n.z-zn);for(let[C,O]of[[-i/2+.1,-s/2+.1],[i/2-.1,-s/2+.1],[-i/2+.1,s/2-.1],[i/2-.1,s/2-.1],[0,-s/2+.1],[0,s/2-.1]])ne(Ce(.15,c,.15),a,t,new y(C,-c/2,O));ne(Ce(i,.1,s),a,t,new y(0,-.05,0));let l=C=>(C.userData.body=1,C);e.parts.basin=l(ne(Ce(i,.55,s,.02),o,t,new y(0,.275,0)));let u=_e.water.clone();u.map=En.water.clone(),u.map.wrapS=u.map.wrapT=oi,u.map.needsUpdate=!0;let d=ne(new cn(i-.08,s-.08),u,t,new y(0,.45,0),[-Math.PI/2,0,0]);d.castShadow=!1,e.parts.water=d;for(let C of[-1,1])l(ne(Ce(i,r-.55,.08),o,t,new y(0,.55+(r-.55)/2,C*s/2)));let f=new ge({color:3359039,roughness:.95});for(let C of[-1,1])l(ne(Ce(.55,r-1.1,s-.3),f,t,new y(C*(i/2-.55),.55+(r-1.1)/2+.05,0)));let p=new ln({map:En.fall.clone(),transparent:!0,opacity:0,depthWrite:!1,side:mn,color:14086399});p.map.wrapS=p.map.wrapT=oi,p.map.repeat.set(7,2),p.map.needsUpdate=!0,e.parts.curtain=p;for(let C of[-1,1])ne(new cn(s-.32,r-1.1),p,t,new y(C*(i/2-.24),.55+(r-1.1)/2,0),[0,Math.PI/2,0]).castShadow=!1;let x=_e.ctLouvre.clone();x.transparent=!0,x.opacity=.55,x.depthWrite=!1;for(let C of[-1,1])l(ne(Ce(.05,r-.95,s-.16),x,t,new y(C*(i/2-.03),.55+(r-.95)/2,0)));l(ne(Ce(i,.1,s),o,t,new y(0,r,0))),e.parts.hot=[];for(let C of[-1,1]){let O=C*i*.3;for(let[k,q,z,ee]of[[i*.36,.04,O,s*.4],[i*.36,.04,O,-s*.4],[.04,s*.8,O-i*.18,0],[.04,s*.8,O+i*.18,0]])ne(Ce(k,.25,q),o,t,new y(z,r+.17,ee));let H=u.clone();H.map=En.water.clone(),H.map.wrapS=H.map.wrapT=oi,H.map.needsUpdate=!0,H.opacity=.9,ne(new cn(i*.35,s*.79),H,t,new y(O,r+.2,0),[-Math.PI/2,0,0]).castShadow=!1,e.parts.hot.push(H)}l(ne(new fr(.86,1.08,.5,48,1,!0),o,t,new y(0,r+.3,0))).material.side=mn;let b=new Oe;b.position.set(0,r+.35,0),t.add(b),e.spin.push({m:b,axis:"y",fan:!0}),e.parts.fan=b;for(let C=0;C<6;C++)ne(Ce(.92,.025,.22),_e.black,b,null,[.22,C*Math.PI/3,0]).position.set(Math.cos(C*Math.PI/3)*.5,0,-Math.sin(C*Math.PI/3)*.5);ne(pt(.14,.22,18),_e.galv,b,null);let g=new ta(new y(0,r+.5,0),new y(0,r+1.25,0),new y(0,r+1.5,-.15),new y(0,r+1.5,-1.15)),m=ne(new jr(g,40,.86,48,!1),o,t);m.material=o.clone(),m.material.side=mn,e.mats.add(m.material);let A=ne(new bi(.86,.045,10,48),o,t,new y(0,r+1.5,-1.15)),U=ne(new $r(.84,40),new ge({color:10134440,metalness:.6,roughness:.5,transparent:!0,opacity:.22,side:mn,depthWrite:!1}),t,new y(0,r+1.5,-1.13));U.castShadow=!1,e.parts.outlet=new y(0,r+1.5,-1.2),l(ne(Ce(.34,.3,.3),fn(e,_e.motor),t,new y(.95,r+.25,-.75))),l(ne(Ce(.24,.2,.14),_e.panel,t,new y(1.15,r+.25,-.45)));let T=_e.yellow,I=r+.06;for(let C of[-s/2+.04,s/2-.04]){ne(Ce(i,.04,.04),T,t,new y(0,I+1.1,C)),ne(Ce(i,.03,.03),T,t,new y(0,I+.55,C)),ne(Ce(i,.1,.015),T,t,new y(0,I+.05,C));for(let O=-i/2+.04;O<=i/2;O+=.86)ne(Ce(.04,1.1,.04),T,t,new y(O,I+.55,C))}let L=n.cell===1?[-1]:[1];for(let C of L){let O=C*(i/2-.04);ne(Ce(.04,.04,s),T,t,new y(O,I+1.1,0)),ne(Ce(.03,.03,s),T,t,new y(O,I+.55,0));for(let H=-s/2+.04;H<=s/2;H+=.86)ne(Ce(.04,1.1,.04),T,t,new y(O,I+.55,H))}if(n.cell===1){let O=s/2+.22,H=-c,k=I+1.1;for(let q of[-.22,.22])ne(Ce(.05,k-H,.05),_e.galv,t,new y(.75+q,(H+k)/2,O));for(let q=H+.3;q<I;q+=.3)ne(pt(.014,.44,8),_e.galv,t,new y(.75,q,O),[0,0,Math.PI/2]);for(let q=H+2.2;q<k;q+=.7)ne(new bi(.36,.014,6,24,Math.PI),_e.galv,t,new y(.75,q,O),[Math.PI/2,0,0])}let P=new ge({map:En.fall.clone(),color:3842264,emissive:741240,emissiveIntensity:.6,transparent:!0,opacity:0,depthWrite:!1,side:mn});P.map.needsUpdate=!0,e.parts.fall=[];for(let C of[-1,1]){let O=ne(new cn(i,1.6),P,t,new y(0,-.3,C*(s/2+.03)));O.castShadow=!1,e.parts.fall.push(O)}e.parts.fallMat=P;let M=ne(new $r(1,40),new ge({color:5935016,roughness:.05,metalness:.3,transparent:!0,opacity:.8}),t,new y(0,-c+.01,0),[-Math.PI/2,0,0]);M.visible=!1,e.parts.puddle=M,e.parts.plume=Ru(70,15922936,1.1,0)}function Yf(n,e,t){let i=ho(n),s=i.g;if(t){ne(pt(Me(n.L)/2,Me(n.H)-.2,36),fn(i,e),s,new y(0,Me(n.H)/2+.1,0)),ne(new Ei(Me(n.L)/2,30,14,0,6.3,0,1.6),fn(i,e),s,new y(0,Me(n.H)-.1,0));for(let r=0;r<3;r++)ne(Ce(.06,.25,.06),_e.steel,s,new y(Math.cos(r*2.1)*.3,.1,Math.sin(r*2.1)*.3))}else if(n.type==="bypass"){for(let r of[-1,1])ne(Ce(.1,Me(n.H),Me(n.W)),fn(i,_e.steel),s,new y(r*(Me(n.L)/2-.1),Me(n.H)/2,0));ne(Ce(Me(n.L),.08,.12),fn(i,_e.steel),s,new y(0,Me(n.H)-.04,0))}else ne(Ce(Me(n.L),Me(n.H),Me(n.W),.03),fn(i,e),s,new y(0,Me(n.H)/2,0));if(n.type==="panel"){let r=Au(256,128);ne(new cn(Me(n.L)*.32,.19),r.mat,s,new y(-.2,1.4,Me(n.W)/2+.021)),i.parts.lcd=r,i.parts.panel=s.children[0],i.parts.leds=[];for(let o=0;o<8;o++)i.parts.leds.push(ne(new Ei(.012,8,6),new ge({color:273,emissive:o%3?2278750:16756768,emissiveIntensity:1}),s,new y(.15+o%4*.05,1.5-Math.floor(o/4)*.05,Me(n.W)/2+.02)))}return i}function D1(n){let e=ho(n),t=e.g,i=Me(n.L),s=Me(n.W),r=Me(n.H),o=fn(e,_e.panel);ne(Ce(i,r,s,.03),o,t,new y(0,r/2,0)),ne(Ce(i*.3,r*.8,.02),new ge({color:8161940,metalness:.6,roughness:.4}),t,new y(-i*.25,r/2,s/2+.011));let a=new Oe;a.position.set(i*.25,r/2,s/2+.02),t.add(a),e.spin.push({m:a,axis:"z",fan:!0}),ne(new bi(r*.32,.03,8,32),_e.steel,t,new y(i*.25,r/2,s/2+.02));for(let l=0;l<5;l++)ne(Ce(r*.55,.07,.02),_e.black,a,null,[0,0,l*Math.PI/5]);let c=Au(256,96);return ne(new cn(.5,.19),c.mat,t,new y(-i*.25,r*.85,s/2+.03)),e.parts.lcd=c,e}function N1(n){let e=ho(n),t=e.g;ne(Ce(Me(n.L),Me(n.H),Me(n.W),.02),fn(e,_e.panel),t,new y(0,Me(n.H)/2,0));let i=new Oe;i.position.set(0,-.01,0),t.add(i),e.spin.push({m:i,axis:"y",fan:!0});for(let s=0;s<3;s++)ne(Ce(.5,.01,.06),_e.black,i,null,[0,s*1.05,0]);return e}function U1(n){let e=ho(n),t=e.g,i=Me(n.L);ne(pt(i/2,Me(n.H),28),fn(e,_e.galv),t,new y(0,Me(n.H)/2,0));let s=new Oe;s.position.set(0,Me(n.H)+.02,0),t.add(s),e.spin.push({m:s,axis:"y",fan:!0});for(let r=0;r<4;r++)ne(Ce(i*.8,.02,.12),_e.black,s,null,[0,r*Math.PI/4,0]);return e}for(let n of[...Qe.equipment,...Qe.air_equipment])n.type==="chiller"?I1(n):n.type==="pump"?P1(n):n.type==="ct"?L1(n):n.type==="ahu"?D1(n):n.type==="fcu"?N1(n):n.type==="fan"?U1(n):n.type==="exptank"?Yf(n,_e.red,!0):n.type==="panel"?Yf(n,_e.panel):Yf(n,_e.galv);var $f={},Mu={};function oo(n,e){let t=(window.GLB_URL||{})[n];if(t){if($f[n])return e($f[n]);(Mu[n]=Mu[n]||[]).push(e),!(Mu[n].length>1)&&fetch(window.ALT_URL("alt79/"+t)).then(i=>{if(!i.ok)throw new Error("HTTP "+i.status);return i.arrayBuffer()}).then(i=>new gu().parse(i,"",s=>{let r=s.scene;r.traverse(o=>{o.isMesh&&(o.castShadow=o.receiveShadow=!0)}),$f[n]=r,Mu[n].forEach(o=>o(r))},s=>console.warn("GLB "+n,s))).catch(i=>console.warn("GLB "+n+" not loaded (procedural model kept)",i))}}var F1={chiller:[3.774,1.771,2.033],pump:[1.75,.65,.85],ahu:[3.6,1.8,2.1],oau:[4.2,2,2.2],tower:[2.6,2.6,2.7],roof_fan:[1.2,1.2,1.1],exptank:[.9,.9,1.6],bypass:[1.3,.5,1.04],panel:[2.4,.5,2.1]};function va(n,e,t,i){let s=Me(n.e.L),r=Me(n.e.W),o=Me(n.e.H),a=F1[i||n.e.type],c=n.e.type==="ct";for(let d of[...n.g.children])(!c||d.userData.body)&&n.g.remove(d);let l=e.clone(!0);l.scale.set(s/a[0],o/a[2],r/a[1]),n.g.add(l),c||n.mats.clear(),l.traverse(d=>{d.isMesh&&(d.material=d.material.clone(),n.mats.add(d.material))});let u=d=>l.getObjectByName(d);for(let[d,f]of Object.entries(t)){let p=u(f);p&&(n.parts[d]=p)}if(n.parts.screen&&n.parts.lcd&&(n.parts.screen.material=n.parts.lcd.mat),n.parts.comp&&(n.parts.compY=n.parts.comp.position.y),c){n.parts.basin=u("casing")||n.parts.basin,n.ghost=void 0;return}if(n.spin=[],n.e.type==="pump")for(let d of["motorFan","shaft"]){let f=u(d);f&&n.spin.push({m:f,axis:"x"})}if(n.e.type==="ahu"){let d=u("fanWheel");d&&n.spin.push({m:d,axis:"z",fan:!0})}if(n.e.type==="fan"){let d=u("fanWheel");d&&n.spin.push({m:d,axis:"y",fan:!0})}if(n.e.type==="panel"){let d=u("pilots");n.parts.leds=[],d&&d.traverse(f=>{f.isMesh&&n.parts.leds.push(f)})}if(n.e.type==="panel"||n.e.type==="ahu"){let d=u("screen");d&&n.parts.lcd&&(d.material=n.parts.lcd.mat)}n.ghost=void 0}for(let n in zt){let e=zt[n],t=e.e.type;if(t==="chiller")oo("chiller",i=>va(e,i,{comp:"comp",evap:"evap",cond:"cond",panel:"panel",screen:"screen",beacon:"beacon"}));else if(t==="pump")oo("pump",i=>va(e,i,{motor:"motor",volute:"volute"}));else if(t==="ahu"){let i=e.e.L>3600?"oau":"ahu";oo(i,s=>va(e,s,{screen:"screen"},i))}else t==="ct"?oo("tower",i=>va(e,i,{},"tower")):t==="fan"?oo("roof_fan",i=>va(e,i,{},"roof_fan")):(t==="exptank"||t==="bypass"||t==="panel")&&oo(t,i=>va(e,i,{panel:"cabinet"},t))}ne(Ce(Me(Qe.ct_span[1]-Qe.ct_span[0])+3,.25,3.2),_e.steel,Tr,wt((Qe.ct_span[0]+Qe.ct_span[1])/2,6e3,zn+900));ne(Ce(Me(Qe.ct_span[1]-Qe.ct_span[0])+3,.05,.9),new ge({color:7041912,metalness:.6,roughness:.5}),Tr,wt((Qe.ct_span[0]+Qe.ct_span[1])/2,4100,zn+30));var Hi={},xg=new y(0,1,0),Bl=n=>Me(n*25.4/2*1.08),vg=n=>Qe.service[n][2]?.045:0,O1={CHS:1929174,CHR:4629232,CDS:1740720,CDR:3843780,D:8030864,MU:5224928},B1="varying vec2 vUv; varying vec3 vN; varying vec3 vV; void main(){ vUv=uv; vec4 mv=modelViewMatrix*vec4(position,1.); vV=-mv.xyz; vN=normalMatrix*normal; gl_Position=projectionMatrix*mv; }",H1=`uniform float ph,len,off,s0,s1,on,ice; uniform vec3 col; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+1.),f.x),f.y);}
void main(){ float s=off+vUv.x*len; float act=on*step(s0,s)*step(s,s1); float u=s-ph*act; float a=vUv.y*6.2832; vec2 q=vec2(cos(a),sin(a));
 float n=n2(vec2(u*2.4,q.x*2.+q.y*1.3+7.))*.6+n2(vec2(u*6.5,q.y*3.-q.x*2.))*.4;
 float st=smoothstep(.55,.95,n2(vec2(u*1.15,q.x*5.+q.y*5.)));
 float bub=step(.993,h(floor(vec2(u*24.,vUv.y*40.))))*act;
 vec3 N=normalize(vN),Vd=normalize(vV); float fr=pow(1.-abs(dot(N,Vd)),2.5); float lam=.55+.45*max(dot(N,normalize(vec3(.3,1.,.4))),0.);
 vec3 c=col*(.45+.55*n)*lam+vec3(.75,.92,1.)*(st*.45*(.35+.65*act)+bub)+fr*vec3(.3,.45,.55);
 c=mix(c,vec3(.86,.94,1.)*(.8+.2*n),ice); c*=mix(.5,1.,max(act,ice));
 gl_FragColor=vec4(c,1.);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`;function k1(n,e){let t=0;for(let i=0;i<n.length-1;i++){let s=n[i].distanceTo(n[i+1]);if(t+s>=e){let r=n[i].clone().lerp(n[i+1],(e-t)/s);return[[...n.slice(0,i+1),r],[r,...n.slice(i+1)]]}t+=s}return[n,null]}function V1(n,e){let t=new ll,i=n[0].clone();for(let s=1;s<n.length;s++){let r=n[s];if(s<n.length-1){let o=n[s+1],a=r.clone().sub(i).normalize(),c=o.clone().sub(r).normalize();if(a.dot(c)<.999){let l=Math.min(e,r.distanceTo(i)*.48,o.distanceTo(r)*.48),u=r.clone().addScaledVector(a,-l),d=r.clone().addScaledVector(c,l);u.distanceTo(i)>1e-4&&t.add(new Zr(i,u)),t.add(new Kr(u,r.clone(),d)),i=d;continue}}r.distanceTo(i)>1e-4&&t.add(new Zr(i,r.clone())),i=r.clone()}return t}var z1=n=>{let[,e,t]=Qe.service[n];return new ge(t?{color:14212577,metalness:.78,roughness:.33}:{color:new ke(e),metalness:.3,roughness:.42})};for(let n of Qe.pipes){let e=new Oe;jt.piping.add(e),n.floor!==void 0&&n.floor!==null&&Vn(n.floor,e);let t=vg(n.svc),i=z1(n.svc),s={p:n,g:e,mat:i,rad:Bl(n.dn)+t,wm:[],ph:0,segs:[],waters:[]},r=n.pts.map(c=>wt(...c)),o=Qe.valves.find(c=>c.pipe===n.id&&c.kind.startsWith("RED_")),a=[[r,n.dn,0]];if(o){let c=Me(o.s),[l,u]=k1(r,c);a=o.kind==="RED_C"?[[l,o.dn,0],[u,n.dn,c]]:[[l,n.dn,0],[u,o.dn,c]]}for(let[c,l,u]of a){let d=Bl(l),f=V1(c,Math.max(.15,Me(l*25.4*1.5))),p=f.getLength(),x=Math.max(6,Math.ceil(p/.05)),b=new Un({uniforms:{ph:{value:0},len:{value:p},off:{value:u},s0:{value:Me(n.span[0])},s1:{value:Me(n.span[1])},on:{value:0},ice:{value:0},col:{value:new ke(O1[n.svc])}},vertexShader:B1,fragmentShader:H1});s.wm.push(b);let g=new dn(new jr(f,x,d*.84,14,!1),b);e.add(g),s.waters.push(g);let m=ne(new jr(f,x,d+t,22,!1),i,e);s.segs.push(m);for(let A=.7;A<p-.3;A+=3)ne(new fr(d+t+.005,d+t+.005,.16,22,1,!0),kl[n.svc+"_band"],e,f.getPointAt(A/p)).quaternion.setFromUnitVectors(xg,f.getTangentAt(A/p))}Hi[n.id]=s}var Fl=new ge({color:9279132,metalness:.7,roughness:.45}),G1=n=>{if(n<0)return-800;if(n<Ve.f1_h)return Ve.f1_h-Ve.slab;for(let e=2;e<=Ve.floors;e++)if(n<ls(e)+Ve.typ_h)return ls(e)+Ve.typ_h-Ve.slab;return zn},W1=n=>{if(n<0)return-6e3;if(n>=zn)return zn;if(n<Ve.f1_h)return 0;for(let e=Ve.floors;e>=2;e--)if(n>=ls(e))return ls(e);return 0},X1=[...Array(Ve.floors-1).keys()].map(n=>ls(n+2)).concat([zn]);for(let n of Qe.pipes){let e=Hi[n.id].rad,t=n.pts,i=Hi[n.id].g;for(let s=0;s<t.length-1;s++){let[r,o]=[t[s],t[s+1]],a=Math.hypot(o[0]-r[0],o[1]-r[1]);if(Math.abs(r[2]-o[2])>1){let d=Math.min(r[2],o[2]),f=Math.max(r[2],o[2]);for(let p of X1.map(x=>x+300).filter(x=>x>d+200&&x<f-200))ne(new bi(e+.02,.018,8,24),Fl,i,wt(r[0],r[1],p),[Math.PI/2,0,0]);continue}if(a<600)continue;let c=r[2],l=G1(c),u=W1(c);for(let d=500;d<a-300;d+=c>zn?2500:3e3){let f=r[0]+(o[0]-r[0])*d/a,p=r[1]+(o[1]-r[1])*d/a,x=Math.atan2(o[1]-r[1],o[0]-r[0]);c>zn?ne(Ce(.6,Math.max(.05,Me(c-zn)-e),.25),_e.concrete,i,wt(f,p,(zn+c-e*1e3)/2),[0,x,0]):c-u>=1500?(ne(pt(.009,Me(l-c),6),Fl,i,wt(f,p,(l+c)/2)),ne(new bi(e+.015,.012,6,24),Fl,i,wt(f,p,c),[0,-x,0])):(ne(pt(.045,Me(c-u)-e,10),Fl,i,wt(f,p,(c-e*1e3+u)/2)),ne(Ce(.3,.02,.3),Fl,i,wt(f,p,u+10)))}}}var Vl=[],zl={},q1=wt(Kt.x/2,Kt.y/2,0);function Y1(n,e,t){let i=e.clone().normalize(),s=t?new y(t[0],t[2],-t[1]):Math.abs(i.y)>.9?q1.clone().sub(n).setY(0).normalize():xg.clone();return s.sub(i.clone().multiplyScalar(s.dot(i))).normalize(),new rn().setFromRotationMatrix(new rt().makeBasis(s,i,new y().crossVectors(s,i)))}var $1=new ge({color:1382170,roughness:.9}),Z1=Zn(128,128,n=>{n.fillStyle="#f4f4f0",n.beginPath(),n.arc(64,64,62,0,7),n.fill(),n.strokeStyle="#222",n.lineWidth=3;for(let e=0;e<=10;e++){let t=Math.PI*(.75+e*.15);n.beginPath(),n.moveTo(64+Math.cos(t)*50,64+Math.sin(t)*50),n.lineTo(64+Math.cos(t)*58,64+Math.sin(t)*58),n.stroke()}n.fillStyle="#b91c1c",n.fillRect(96,90,14,6)}),K1=new ln({map:Z1});function As(n,e,t){ne(pt(e*1.55,.028,28),_e.iron,n,new y(0,t,0))}for(let n of Qe.valves){let e=Hi[n.pipe];if(!e||n.hidden)continue;let t=e.p.dn,i=vg(e.p.svc),s=Bl(n.dn||t),r=wt(...n.xyz),o=wt(...n.dir).sub(wt(0,0,0)).normalize(),a=new Oe;a.position.copy(r),a.quaternion.copy(Y1(r,o,n.stem)),e.g.add(a),a.position.sub(e.g.position);let c={v:n,g:a,pos:["BFV"].includes(n.kind)?1:0,tgt:1,k:n.kind,pr:e},l=n.kind;if(["BFV","MBFV","MCV","CHECK"].includes(l)){if(As(a,s,-.045),As(a,s,.045),ne(pt(s*1.3,l==="CHECK"?.11:.07,28),_e.iron,a),l!=="CHECK"?(c.disc=ne(pt(s*.96,.014,28),_e.galv,a),ne(pt(.028,s*.5+.1,10),_e.galv,a,new y(s*1.3+.04,0,0),[0,0,Math.PI/2])):ne(Ce(.05,.05,.05),_e.iron,a,new y(s*1.3,0,0)),l==="BFV"){let u=new Oe;u.position.set(s*1.3+.1,0,0),a.add(u);let d=Math.max(.24,s*2.2);ne(Ce(.04,.05,.05),_e.iron,u),ne(Ce(.02,d,.035),_e.red,u,new y(.02,d/2-.03,0)),c.ind=u}if(l==="MBFV"||l==="MCV"){let u=new Oe;u.position.set(s*1.3+.12,0,0),a.add(u),c.act=u;let d=new ge({color:l==="MCV"?2842272:6253432,metalness:.45,roughness:.4});c.am=d,ne(Ce(.17,.24,.22,.025),d,u,new y(.085,0,0)),ne(Ce(.05,.06,.06),_e.black,u,new y(.11,-.14,.06));let f=new Oe;f.position.set(.18,0,0),u.add(f),ne(pt(.07,.02,28),new ge({color:987413,transparent:!0,opacity:.85}),f,null,[0,0,Math.PI/2]),ne(Ce(.014,.11,.024),_e.yellow,f,new y(.012,.02,0)),ne(Ce(.014,.03,.05),_e.yellow,f,new y(.012,.07,0)),c.ind=f,c.led=ne(new Ei(.016,10,8),new ge({color:273,emissive:2278750,emissiveIntensity:1.5}),u,new y(.13,.1,.112))}}else if(l==="STRAINER"){As(a,s,-s*1.3),As(a,s,s*1.3),ne(pt(s*1.18,s*2.5,26),_e.iron,a);let u=ne(pt(s*.75,s*2.1,22),_e.iron,a,new y(-s*.95,s*.55,0),[0,0,Math.PI/4]);ne(pt(s*.85,.03,22),_e.iron,u,new y(0,s*1.05,0)),ne(pt(.012,.1,8),_e.galv,u,new y(0,s*1.05+.05,0))}else if(l==="FLEX"){As(a,s,-s*.95),As(a,s,s*.95);let u=new Oe;a.add(u),c.flex=u;for(let d of[-s*.32,s*.32])ne(new Ei(s*1.28,24,14),$1,u,new y(0,d,0)).scale.set(1,.62,1);for(let d=0;d<4;d++){let f=d*Math.PI/2+Math.PI/4;ne(pt(.008,s*2.1,6),_e.galv,a,new y(Math.cos(f)*s*1.45,0,Math.sin(f)*s*1.45))}}else if(l==="RED_E"||l==="RED_C"){let u=Bl(t),d=Bl(n.dn),f=l==="RED_E"?u:d,p=l==="RED_E"?d:u,x=Math.max(.12,(u-d)*6),b=new fr(p,f,x,28);if(l==="RED_E"){let g=b.attributes.position;for(let m=0;m<g.count;m++)g.getY(m)<0&&g.setX(m,g.getX(m)-(u-d));g.needsUpdate=!0,b.computeVertexNormals()}ne(b,kl[e.p.svc]||_e.iron,a),As(a,p,x/2),As(a,f,-x/2)}else if(l==="FM"){As(a,s,-s*1.1),As(a,s,s*1.1),ne(pt(s*1.2,s*2,28),new ge({color:2778280,metalness:.4,roughness:.4}),a),ne(pt(.04,.12,10),_e.galv,a,new y(s*1.2+.06,0,0),[0,0,Math.PI/2]);let u=Au(192,96);ne(Ce(.12,.18,.14,.02),_e.panel,a,new y(s*1.2+.17,0,0)),ne(new cn(.1,.065),u.mat,a,new y(s*1.2+.17,.02,.071)),c.lcd=u}else if(l==="PG"){ne(pt(.009,s+i+.08,8),_e.galv,a,new y((s+i)/2+.04,0,0),[0,0,Math.PI/2]);let u=new Oe;u.position.set(s+i+.13,0,0),a.add(u),ne(pt(.055,.03,28),_e.galv,u,null,[Math.PI/2,0,0]),ne(new $r(.05,28),K1,u,new y(0,0,.016));let d=new Oe;d.position.z=.018,u.add(d),ne(Ce(.004,.042,.003),_e.black,d,new y(0,.018,0)),c.needle=d}else if(["TT","FS","PT"].includes(l))ne(pt(.012,s+i+.06,8),_e.galv,a,new y((s+i)/2+.03,0,0),[0,0,Math.PI/2]),ne(l==="TT"?pt(.035,.05,16):Ce(.08,.09,.08),l==="FS"?_e.motor:_e.panel,a,new y(s+i+.1,0,0),l==="TT"?[0,0,Math.PI/2]:null),l==="FS"&&(c.led=ne(new Ei(.01,8,6),new ge({color:273,emissive:2278750,emissiveIntensity:0}),a,new y(s+i+.1,.03,.042)));else if(l==="AAV"){a.quaternion.identity();let u=Math.abs(o.y)>.9?.02:s+i;ne(pt(.012,.06,8),_e.galv,a,new y(0,u+.03,0)),ne(pt(.03,.07,14),_e.galv,a,new y(0,u+.09,0))}else if(l==="CAP"){let u=n.s<1?-1:1;ne(pt(s*1.55,.03,28),_e.iron,a,new y(0,u*.015,0)),ne(pt(s*1.55,.03,28),_e.iron,a,new y(0,u*.045,0))}else l==="DRAIN"&&(ne(pt(.016,.14,8),_e.galv,a,new y(-1*(s+.06),0,0),[0,0,Math.PI/2]),ne(Ce(.03,.1,.015),_e.red,a,new y(-1*(s+.1),.04,0)));n.pt&&(zl[n.pt]=c),Vl.push(c)}function Ru(n,e,t,i,s){let r=new tn;r.setAttribute("position",new Dt(new Float32Array(n*3),3));let o=new ur({color:e,size:t,map:En.soft,transparent:!0,opacity:i,depthWrite:!1,blending:s||Ui,sizeAttenuation:!0}),a=new Yr(r,o);return a.frustumCulled=!1,a.userData.seed=Float32Array.from({length:n},Math.random),_n.add(a),a}var yr=new hr(new tn,new zs({color:11456480,transparent:!0,opacity:0}));{let e=new Float32Array(36e3);for(let t=0;t<6e3;t++){let i=Math.random()*160-48,s=Math.random()*70,r=Math.random()*160-100;e.set([i,s,r,i+.04,s-.55,r],t*6)}yr.geometry.setAttribute("position",new Dt(e,3)),yr.frustumCulled=!1,_n.add(yr)}var yg=[];for(let n=0;n<46;n++){let e=new es(new Li({map:En.cloud,transparent:!0,opacity:0,depthWrite:!1,fog:!1})),t=Math.random()*6.28,i=120+Math.random()*520;e.position.set(Math.cos(t)*i,70+Math.random()*90,Math.sin(t)*i),e.scale.set(220+Math.random()*180,70+Math.random()*50,1),_n.add(e),yg.push(e)}var ep=Ru(1200,16777215,2.2,0);{let n=ep.geometry.attributes.position.array;for(let e=0;e<1200;e++){let t=Math.random()*6.28,i=Math.random()*1.3;n.set([Math.cos(t)*Math.cos(i)*1500,Math.sin(i)*1500+40,Math.sin(t)*Math.cos(i)*1500],e*3)}ep.material.sizeAttenuation=!1}var tp=new Un({transparent:!0,depthWrite:!1,uniforms:{t:{value:0},k:{value:0}},vertexShader:"varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }",fragmentShader:"varying vec2 vUv; uniform float t,k; void main(){ float w=sin(vUv.y*60.+t*4.)*sin(vUv.x*22.-t*2.); float a=k*(.07+.06*w)*(1.-vUv.y); gl_FragColor=vec4(1.,.82,.6,a); }"}),Mg=new dn(new cn(26,9),tp);Mg.position.set(pg/2,w1+6,-mg/2+6);_n.add(Mg);var eg={};function Zf(n){return eg[n]||(eg[n]={})}function j1(n,e){let t=document.createElement("canvas"),i=t.getContext("2d");t.width=t.height=128,i.fillStyle=e,i.beginPath(),i.arc(64,64,58,0,7),i.fill(),i.strokeStyle="#fff",i.lineWidth=8,i.fillStyle="#fff",i.font='700 74px "Segoe UI",sans-serif',i.textAlign="center",i.textBaseline="middle",n==="maint"?(i.lineCap="round",i.beginPath(),i.moveTo(40,88),i.lineTo(78,50),i.stroke(),i.beginPath(),i.arc(84,44,16,-.6,3.6),i.stroke()):i.fillText({sensor:"?",hand:"H",perf:"!",chem:"C",airside:"!",valve:"V",pressure:"P"}[n]||"!",64,70);let s=new es(new Li({map:new ci(t),depthTest:!1,transparent:!0}));return s.scale.set(.75,.75,1),s.renderOrder=10,s}function Ea(n){let e=zt[n],t=new un().setFromObject(e.g);return new y((t.min.x+t.max.x)/2,t.max.y+.5,(t.min.z+t.max.z)/2)}function Kf(n){return new un().setFromObject(zt[n].g).getCenter(new y)}function tg(n){return Object.values(Hi).filter(e=>e.p.eq.includes(n))}var mt={},ki=!1,jn=new Map,as=new Set,js={on:!1,temp:33,rh:60,hour:13};function Er(n,e){let t=mt[n];return typeof t=="number"&&!isNaN(t)?t:typeof t=="boolean"?+t:e}var np={},pp=!1;function kn(n,e,t){let i=Er(n,pp?NaN:t);return Number.isFinite(i)?i.toFixed(e):"\u2014"}function Eg(){let n=new Date,e={temp:Er("OA_Temperature",33),rh:Er("OA_Humidity",62),wb:Er("OA_WetBulb",27),hour:n.getHours()+n.getMinutes()/60};return js.on&&Object.assign(e,{temp:js.temp,rh:js.rh,hour:js.hour,wb:js.temp-(100-js.rh)/5*.9}),e.night=e.hour<6.1||e.hour>18.6,e.rain=e.rh>=92&&e.temp<=30,e.fog=e.rh>=95&&(e.hour<9||e.night),e.hot=e.temp>=36,e.cover=Math.max(0,Math.min(1,(e.rh-50)/40))+(e.rain?.3:0),e.label=e.night?e.rain?"Night rain":"Night":e.rain?"Rain":e.fog?"Mist":e.hot?"Very hot, strong sun":e.cover>.65?"Overcast":e.cover>.3?"Partly cloudy":"Clear sky",e}var ng="";function ip(n,e){let t=Zs.degToRad(Math.max(-20,78*Math.sin(Math.PI*(n.hour-6.2)/12.4))),i=Zs.degToRad(90+(n.hour-6)/12*180),s=new y().setFromSphericalCoords(1,Math.PI/2-t,i);er.sunPosition.value.copy(s),er.turbidity.value=4+n.cover*10+(n.hot?4:0),er.rayleigh.value=n.night?.2:1.4+n.cover*1.5,wi.position.copy(s.clone().multiplyScalar(90)).add(wi.target.position);let r=Math.max(0,Math.sin(t)),o=1-n.cover*.65;wi.intensity=(n.night?0:3.4*Math.min(1,r*2.2))*o,wi.color.setHSL(.09+.04*r,.55,.62+.25*r),bu.intensity=n.night?.22:.45+.3*r,bu.color.set(n.cover>.6?12109004:13624319),Fn.toneMappingExposure=n.night?.5:.58+.08*(1-n.cover),ep.material.opacity=n.night?.85*(1-n.cover):0,hg.forEach(c=>c.intensity=n.night||n.cover>.9?60:0),T1.material.emissiveIntensity=n.night?.9:.05,yg.forEach((c,l)=>{c.material.opacity=Math.min(.95,n.cover*(.45+l%5*.12)),c.material.color.set(n.rain?9213083:n.night?4212559:16777215),c.position.x+=Math.sin(l)*.02}),yr.material.opacity=n.rain?.55:0,b1.forEach(c=>{c.roughness=n.rain?.18:c===_e.slab?.9:c.map===En.asphalt?.85:1,c.color.set(n.rain?9080724:16777215)}),_n.fog=n.fog?new Wr(13620956,.0055):n.rain?new Wr(9082269,.006):new Wr(n.night?857376:10466244,9e-4),tp.uniforms.k.value=n.hot?Math.min(1,(n.temp-35)/4):0,tp.uniforms.t.value=e;let a=[Math.round(n.hour*4),Math.round(n.cover*5),n.rain,n.night].join("|");a!==ng&&(ng=a,_n.environment=E1.fromScene(J1(),.04).texture),tt("wx").innerHTML=`<b>${n.label}</b><span>${kn("OA_Temperature",1,n.temp)} \xB0C \xB7 RH ${kn("OA_Humidity",0,n.rh)}% \xB7 WB ${kn("OA_WetBulb",1,n.wb)} \xB0C \xB7 ${String(Math.floor(n.hour)).padStart(2,"0")}:${String(Math.floor(n.hour%1*60)).padStart(2,"0")}</span>`}var bg=new jo,mp=new ga;mp.scale.setScalar(1e3);bg.add(mp);function J1(){for(let n in er)mp.material.uniforms[n].value=er[n].value;return bg}var Tg=["power","fire","leak","freeze","overflow","lowlevel","overheat","noflow","trip","vibration","pressure","valve","chem","sensor","hand","maint","perf","airside"];function Q1(n){let e={};for(let o of jn.values())for(let a of o.e)(e[a]=e[a]||new Set).add(o.x);let t=new Set([...jn.values()].map(o=>o.x)),i=.5+.5*Math.sin(n*6);for(let o in zt){let a=zt[o],c=a.ghost?new Set:e[o]||new Set,l=Zf(o),u=0,d=0;if(c.has("trip")||c.has("noflow")?(u=16718352,d=.55*i):c.has("overheat")?(u=16734736,d=.8*(.6+.4*i)):c.has("freeze")?(u=7324671,d=.35):c.size&&[...c].some(p=>!["maint","hand","sensor","perf"].includes(p))&&(u=16752640,d=.25*i),a.mats.forEach(p=>{p.emissive&&p.emissive.setHex(u),p.emissiveIntensity=d}),c.has("freeze")&&a.parts.evap?(l.frost||(l.frost=new dn(a.parts.evap.geometry,new ge({color:15333119,roughness:.25,metalness:0,transparent:!0,opacity:.8,emissive:10475775,emissiveIntensity:.25})),l.frost.scale.setScalar(1.06),a.parts.evap.add(l.frost),l.snow=Ru(500,16777215,.05,.9)),l.frost.visible=!0,Sg(l.snow,Kf(o),2.2,1.4,n,-.4,.9)):(l.frost&&(l.frost.visible=!1),l.snow&&(l.snow.visible=!1)),ya(l,"heat",c.has("overheat"),16747072,.35,.5,oa,Ea(o),.9,1.2,n,.7),ya(l,"smoke",c.has("trip")||c.has("fire"),7172469,.32,.9,Ui,Ea(o),.8,3,n,.4),ya(l,"gas",c.has("leak"),13172696,.9,.35,Ui,Kf(o),3.2,1.6,n,.12),a.g.position.copy(a.base),c.has("vibration")||c.has("trip")&&o.startsWith("C")){let p=c.has("vibration")?.02:.006;a.g.position.x+=(Math.random()-.5)*p,a.g.position.z+=(Math.random()-.5)*p}if(a.parts.water&&!a.ghost){let p=c.has("overflow"),x=c.has("lowlevel");a.parts.water.position.y=p?.56:x?.07:.45,a.parts.water.material.color.set(x?8014394:p?10473696:9418948),a.parts.fallMat.opacity=p?.9:0,a.parts.fallMat.map.offset.y=n*1.6%1,a.parts.puddle.visible=p,a.parts.puddle.scale.setScalar(p?2.2+Math.sin(n)*.1:1),ya(l,"splash",p,15267839,.95,.14,Ui,a.g.position.clone().add(new y(0,.55,1.35)),2.4,.9,n,-.6)}let f=["sensor","hand","maint","perf","chem","valve","pressure","airside"].find(p=>c.has(p));f&&o!=="BUILDING"?((!l.icon||l.iconKind!==f)&&(l.icon&&_n.remove(l.icon),l.icon=j1(f,f==="sensor"?"#6b7280":f==="maint"?"#c99400":f==="hand"?"#2563eb":"#d97706"),l.iconKind=f,_n.add(l.icon)),l.icon.visible=!0,l.icon.position.copy(Ea(o)).add(new y(0,.5+.1*Math.sin(n*3),0)),l.icon.material.opacity=f==="sensor"?Math.random()<.85?1:.2:1):l.icon&&(l.icon.visible=!1)}for(let o of Object.values(Hi))o.mat.emissive.setHex(0),o.g.scale.set(1,1,1),o.noflow=!1,o.ice=!1;for(let o in e){let a=e[o];for(let c of tg(o))a.has("noflow")&&(c.mat.emissive.setHex(16719888),c.mat.emissiveIntensity=.7*i,c.noflow=!0),a.has("pressure")&&(c.mat.emissive.setHex(16738816),c.mat.emissiveIntensity=.5*i),a.has("freeze")&&/^CH[SR]/.test(c.p.id)&&(c.ice=!0)}let s=new Set(Object.keys(e).filter(o=>e[o].has("valve")).flatMap(o=>tg(o).map(a=>a.p.id)));Vl.forEach(o=>{o.bad=!!o.act&&s.has(o.v.pipe),o.am&&(o.am.emissive.setHex(o.bad?16719888:0),o.am.emissiveIntensity=o.bad?i:0)});let r=t.has("power");_g.forEach(o=>o.intensity=r?Math.sin(n*10)>.6?0:1.5:7),gp.intensity=r||t.has("fire")?60*(Math.sin(n*8)>0?1:0):0,ya(Zf("CP-01"),"spark",r,16769162,1,.06,oa,Kf("CP-01").add(new y(0,.6,.3)),.5,.6,n,1.8),ya(Zf("ROOM"),"roomsmoke",t.has("fire"),6975090,.45,1.2,Ui,wt(Kt.x/2,Kt.y/2,2500),14,3,n,.1),sp.clear();for(let o of jn.values())for(let a of o.e)a.startsWith("Z-")&&sp.add(a.slice(2))}function ya(n,e,t,i,s,r,o,a,c,l,u,d){if(!t){n[e]&&(n[e].visible=!1);return}n[e]||(n[e]=Ru(160,i,r,s,o)),Sg(n[e],a,c,l,u,d,s)}function Sg(n,e,t,i,s,r,o){n.visible=!0;let a=n.geometry.attributes.position.array,c=n.userData.seed;for(let l=0;l<c.length;l++){let u=(c[l]+s*Math.abs(r)*.3)%1,d=c[l]*40;a[l*3]=e.x+Math.cos(d)*t*(.2+u*.8)*.5,a[l*3+1]=e.y+(r>=0?u*i:-u*i*1.8),a[l*3+2]=e.z+Math.sin(d)*t*(.2+u*.8)*.5}n.geometry.attributes.position.needsUpdate=!0,n.material.opacity=o}var gp=new Di(16719904,0,30,1.5);gp.position.copy(wt(Kt.x/2,Kt.y/2,4200));Tr.add(gp);function lo(n){let e=zt[n];return!e||!e.e.run||e.ghost?!1:!!mt[e.e.run]}var sp=new Set,Eu=n=>[...jn.values()].some(e=>e.e.includes(n)&&e.x==="trip"),eb=6309e-8,Rs=n=>Object.keys(zt).filter(e=>n.test(e));function tb(n){let e=n.fl||"",t=Er("CHWFlow",0),i=Er("CDW_Flow",0),s=u=>Math.max(1,u.filter(Boolean).length),r=s(Rs(/^CHP-/).map(lo)),o=s(Rs(/^CDP-/).map(lo)),a=s(Rs(/^CH-/).map(u=>mt[`Gfx_${zt[u].e.pt}Evap_Fwd`])),c=s(Rs(/^CH-/).map(u=>mt[`Gfx_${zt[u].e.pt}Cond_Fwd`])),l=s([...new Set(Qe.equipment.filter(u=>u.type==="ct").map(u=>u.tower))].map(u=>mt[`Gfx_${u}_Fwd`]));return/Bypass/.test(e)?t*.12*(zl.Gfx_CHW_BypassMV_Pos?zl.Gfx_CHW_BypassMV_Pos.pos:.2):/AHU_F/.test(e)?t/8:/CHP\d/.test(e)?t/r:/CDP\d/.test(e)?i/o:/Evap_/.test(e)?t/a:/Cond_/.test(e)?i/c:/_CT\d/.test(e)?i/l/2:/^CD/.test(n.svc)?i:t}function nb(){let n=s=>zl[s]?zl[s].pos:0,e=s=>lo(s),t=Rs(/^CHP-/).some(e),i=Rs(/^CDP-/).some(e);Object.assign(mt,{Gfx_ChwMain_Fwd:t,Gfx_EvapTotal_Fwd:t,Gfx_CdwTotal_Fwd:i,Gfx_Bypass_Fwd:t&&n("Gfx_CHW_BypassMV_Pos")>.05});for(let s of Rs(/^C[HD]P-/)){let r=zt[s].e.pt,o=+r.slice(-2);mt[`Gfx_${r}_Fwd`]=e(s)&&n(o<=2?`Gfx_${r}_DischargeMV_Pos`:`Gfx_${r}_MV_Pos`)>.3}for(let s of Rs(/^CH-/)){let r=zt[s].e.pt;mt[`Gfx_${r}Evap_Fwd`]=t&&n(`Gfx_${r}_ChwIso_Pos`)>.3,mt[`Gfx_${r}Cond_Fwd`]=i&&n(`Gfx_${r}_CdwIso_Pos`)>.3}for(let s of new Set(Qe.equipment.filter(r=>r.type==="ct").map(r=>r.tower))){let r=+s.slice(-2);mt[`Gfx_${s}_Fwd`]=i&&n(r<=2?`Gfx_${s}_InletMV_Pos`:`Gfx_${s}_Valve_Pos`)>.3}for(let s=2;s<=Ve.floors;s++)mt[`Gfx_AHU_F${String(s).padStart(2,"0")}_Fwd`]=t&&Er(`AHU_F${String(s).padStart(2,"0")}_ValveCmd`,0)>2}var ig=0;function ib(n,e){ki&&nb();for(let i in zt){let s=zt[i];if(s.ghost)continue;let r=lo(i)&&!Eu(i),o=s.e.pt?Er(s.e.pt+"SpeedCmd",100)/100:1;if(s.spin.forEach(a=>{a.m.rotation[a.axis]+=(r?(a.fan?9:40)*o:0)*e}),s.e.type==="pump"&&r&&(s.g.position.y=s.base.y+Math.sin(n*90)*.0012),s.e.type==="chiller"&&(s.parts.comp.position.y=(s.parts.compY??1.72)+(r?Math.sin(n*70)*.0015:0),s.parts.beacon.material.emissive.setHex(Eu(i)?16719904:2278750),s.parts.beacon.material.emissiveIntensity=Eu(i)?Math.sin(n*8)>0?2.5:0:r?2:0),s.e.type==="ct"){let a=s.e.tower,c=!!mt[`Gfx_${a}_Fwd`]&&!Eu(i),l=Eg();s.parts.curtain.opacity=c?.62:0,s.parts.curtain.map.offset.y=(s.parts.curtain.map.offset.y+e*1.6)%1,s.parts.water.material.map.offset.x+=e*(c?.05:.006),s.parts.water.material.map.offset.y+=e*(c?.03:.004),s.parts.hot.forEach(d=>{d.opacity=c?.9:.25,d.map.offset.y+=e*.08});let u=r?Math.min(1,.15+Math.max(0,(l.rh-55)/45)+Math.max(0,(30-l.temp)/12)):0;if(u>.02){let d=s.g.localToWorld(s.parts.outlet.clone()),f=s.parts.plume;f.visible=!0;let p=f.geometry.attributes.position.array,x=f.userData.seed;for(let b=0;b<x.length;b++){let g=(x[b]+n*.18*o)%1,m=x[b*7%x.length]-.5;p[b*3]=d.x+m*(.5+g*2.2),p[b*3+1]=d.y+g*g*4.5+g*.4,p[b*3+2]=d.z-g*2.6*o+(x[b*3%x.length]-.5)*g*1.5}f.geometry.attributes.position.needsUpdate=!0,f.material.opacity=.14*u,f.material.size=1.4}else s.parts.plume.visible=!1}}Vl.forEach(i=>{if(i.v.pt&&(i.k==="MBFV"||i.k==="MCV")){let a=mt[i.v.pt];typeof a=="boolean"&&(a=a?100:0),typeof a=="number"&&(i.tgt=Math.max(0,Math.min(1,a/100)))}i.bad&&(i.tgt=.45+.25*Math.sin(n*1.7));let s=i.tgt-i.pos,r=Math.abs(s)>.01;i.pos+=Math.sign(s)*Math.min(Math.abs(s),(i.k==="MCV"?.3:.22)*e),i.disc&&(i.disc.rotation.x=i.pos*Math.PI/2),i.ind&&(i.ind.rotation.x=(1-i.pos)*Math.PI/2),i.led&&i.k!=="FS"&&(i.led.material.emissive.setHex(i.bad?16719904:r?16756768:i.pos>.5?2278750:15680580),i.led.material.emissiveIntensity=r||i.bad?Math.sin(n*12)>0?2.5:.2:1.6);let o=i.pr.flow;if(i.k==="FS"&&(i.led.material.emissiveIntensity=o?2:0),i.needle){let a=/-(D\d|DH|C\d|EM|M)$/.test(i.v.pipe)||/^CHR-E|^CDS-C/.test(i.v.pipe)?.75:.35;i.needle.rotation.z=-(o?a+Math.sin(n*23+i.g.id)*.01:.08)*4+2.3}i.flex&&i.flex.scale.setScalar(o?1+Math.sin(n*60)*.012:1)});let t=tt("flow").checked;for(let i in Hi){let s=Hi[i],r=s.p,o=r.fl?mt[r.fl.replace("_Fwd","_Rev")]===!0?-1:mt[r.fl]?1:0:0;s.noflow&&(o=0);let a=Math.PI*(r.dn*.0254/2)**2,c=Math.min(3.5,tb(r)*eb/a);s.flow=!!o,s.ph+=o*c*e,s.wm.forEach(l=>{l.uniforms.ph.value=s.ph,l.uniforms.on.value=o?1:0,l.uniforms.ice.value=s.ice?1:0}),s.clear!==t&&(s.clear=t,s.oc=s.oc||s.mat.color.clone(),s.mat.color.copy(t?new ke(15003123):s.oc),s.mat.metalness=t?.1:Qe.service[r.svc][2]?.78:.3,s.mat.needsUpdate=!0),s.ghost||(s.mat.transparent=t,s.mat.opacity=t?.22:1,s.mat.depthWrite=!t),s.waters.forEach(l=>l.visible=t&&!l.userData.hide)}if((ig+=e)>.5){ig=0,Vl.forEach(s=>{s.lcd&&s.lcd.draw([s.v.tag,kn(s.v.pt,0,0)+" gpm"])});for(let s of Rs(/^CH-/)){if(zt[s].ghost){zt[s].parts.lcd.draw([s,"NOT INSTALLED",""],"#1a1d22","#6b7280");continue}let r=zt[s].e.pt,o=lo(s);zt[s].parts.lcd.draw(o?[`${s} RUN`,`LWT ${kn(r+"_ChwSupplyTemp",1,6.7)} C`,`Load ${kn(r+"LoadPct",0,0)} %`]:[`${s}`,"STANDBY",""],"#061a2a",o?"#7fe3ff":"#8899a6")}for(let s of Rs(/^AHU-/)){let r=zt[s],o=r.e.pt,a=lo(s);r.parts.lcd&&r.parts.lcd.draw([s+(a?" RUN":" OFF"),`Valve ${kn(o+"_ValveCmd",0,0)} %`])}let i=zt["CP-01"];i.parts.lcd.draw(["CPMS "+(ki?"DEMO":"LIVE"),`kW/RT ${kn("Plant_kW_per_RT",2,0)}`,`RT ${kn("CoolingLoad_RT",0,0)}`]),i.parts.leds.forEach((s,r)=>s.material.emissiveIntensity=Math.random()<.7?1.4:0)}sb()}function sb(){let n=tt("kpi");if(!n)return;let e=(t,i)=>kn(t,i,NaN);n.innerHTML=`<div class="big"><span>PLANT EFFICIENCY</span><b>${e("Plant_kW_per_RT",2)}</b><i>kW/RT</i></div>
  <div><span>Cooling load</span><b>${e("CoolingLoad_RT",0)}</b><i>RT</i></div><div><span>Plant power</span><b>${e("Plant_kW",0)}</b><i>kW</i></div>
  <div><span>CHWS / CHWR</span><b>${e("CHWS",1)} / ${e("CHWR",1)}</b><i>\xB0C</i></div><div><span>CDS / CDR</span><b>${e("CDS",1)} / ${e("CDR",1)}</b><i>\xB0C</i></div>
  <div><span>CHW / CDW flow</span><b>${e("CHWFlow",0)} / ${e("CDW_Flow",0)}</b><i>gpm</i></div>`}var Bi={};for(let n of[...Qe.equipment,...Qe.air_equipment]){let e=document.createElement("div");e.className="lbl",e.innerHTML=`<b>${n.id}</b><span></span>`,tt("labels").appendChild(e),e.onclick=()=>_p(n.id),Bi[n.id]=e}var sg=0;function rb(){let n=Hl.clientWidth,e=Hl.clientHeight,t=[];for(let o in Bi){let a=Ea(o).project(Kn),c=Bi[o];c.__p=a;let l=Kn.position.distanceTo(Ea(o))>60&&![...jn.values()].some(p=>p.e.includes(o));if(a.z>1||!tt("labelsOn").checked||l||!zt[o].g.visible||!zt[o].g.parent.visible){c.style.display="none";continue}if(zt[o].ghost){c.style.display="",c.style.transform=`translate(${(a.x+1)/2*n}px,${(1-a.y)/2*e}px) translate(-50%,-100%)`,c.className="lbl ghost",c.querySelector("span").textContent="Not installed (empty slot)",t.push(o);continue}c.style.display="",c.style.transform=`translate(${(a.x+1)/2*n}px,${(1-a.y)/2*e}px) translate(-50%,-100%)`;let u=zt[o],d=[...jn.values()].filter(p=>p.e.includes(o)),f=lo(o);c.className="lbl"+(d.some(p=>["Critical","Emergency"].includes(p.c))?" alm":d.length?" warn":f?" run":""),c.querySelector("span").textContent=d.length?br[d[0].x][0]+(d.length>1?` +${d.length-1}`:""):u.e.pt?f?ob(o):"Off / Standby":"",t.push(o)}let i=performance.now();if(i-sg<150){for(let o of t)Bi[o].__hid&&(Bi[o].style.display="none");return}sg=i;let s=o=>(/ alm/.test(Bi[o].className)?0:/ warn/.test(Bi[o].className)?1e4:2e4)+Kn.position.distanceTo(Ea(o))-(Bi[o].__hid===!1?8:0),r=[];for(let o of t.sort((a,c)=>s(a)-s(c))){let a=Bi[o],c=a.__p,l=(c.x+1)/2*n,u=(1-c.y)/2*e,d=a.offsetWidth,f=a.offsetHeight,p=[l-d/2,u-f,l+d/2,u],x=r.some(b=>p[0]<b[2]+4&&p[2]>b[0]-4&&p[1]<b[3]+2&&p[3]>b[1]-2);a.__hid=x,x?a.style.display="none":r.push(p)}}function ob(n){let e=zt[n].e,t=e.pt;return e.type==="ahu"?`Valve ${kn(t+"_ValveCmd",0,0)}% \xB7 ${e.floor>8?"roof":"floor "+e.floor}`:e.type==="fcu"||e.type==="fan"?"Run":n.startsWith("CH-")?`Load ${kn(t+"LoadPct",0,0)}% \xB7 LWT ${kn(t+"_ChwSupplyTemp",1,6.7)}\xB0C`:`Run \xB7 ${kn(t+"SpeedCmd",0,0)}%`}function _p(n){let e=[...Qe.equipment,...Qe.air_equipment].find(i=>i.id===n),t=Is.filter(i=>i.e.includes(n));tt("info").innerHTML=`<h3>${n}</h3><table>${Object.entries(e.data).map(([i,s])=>`<tr><td>${i}</td><td>${s}</td></tr>`).join("")}</table>
  <h4>Alarms of this unit (${t.length})</h4><div class="alist">${t.map(i=>`<div class="${jn.has(i.n)?"on":""}" data-n="${i.n}"><i>${br[i.x][0]}</i>${i.t}</div>`).join("")}</div>`,tt("info").className="open",tt("info").querySelectorAll("[data-n]").forEach(i=>i.onclick=()=>{ki&&xp(i.dataset.n),_p(n)})}function Cu(){let n=[...jn.values()];tt("acount").textContent=n.length,tt("acount").className=n.length?"n on":"n",tt("alist").innerHTML=n.length?n.map(e=>`<div class="${e.c}"><b>${e.e.join(", ")}</b> ${e.t}<i>${br[e.x][0]} / ${br[e.x][1]}</i></div>`).join(""):'<div class="none">No active alarm</div>'}function xp(n,e){let t=Is.find(i=>i.n===n);t&&(e??!jn.has(n)?jn.set(n,t):jn.delete(n),Cu())}var co=new _l,Gl=new Pe;Fn.domElement.addEventListener("dblclick",n=>{let e=Fn.domElement.getBoundingClientRect();Gl.set((n.clientX-e.left)/e.width*2-1,-(n.clientY-e.top)/e.height*2+1),co.setFromCamera(Gl,Kn);let t=co.intersectObjects([...Tr.children,...jt.air.children],!0)[0],i=t&&t.object;for(;i&&!i.userData.eq;)i=i.parent;if(i){let r=new un().setFromObject(i).getCenter(new y),o=Kn.position.clone().sub(Gn.target).setLength(9);return Qs(r.clone().add(o).toArray(),r.toArray()),_p(i.userData.eq)}let s=co.intersectObjects(jt.zones.children,!0).find(r=>r.object.userData.zone);if(s){let r=s.object.position,o=Kn.position.clone().sub(Gn.target).setLength(22);Qs(r.clone().add(o).toArray(),r.toArray()),ab(s.object.userData.zone)}});function ab(n){let e=Sr[n].z,t=Is.filter(i=>i.e.includes("Z-"+n));tt("info").innerHTML=`<h3>Zone ${n} \xB7 ${e.name}</h3><table><tr><td>Floor</td><td>${e.floor}</td></tr><tr><td>Temperature</td><td>${kn(e.t,1,NaN)} \xB0C</td></tr><tr><td>Humidity</td><td>${kn(e.h,0,NaN)} %RH</td></tr><tr><td>CO2</td><td>${kn(e.c,0,NaN)} ppm</td></tr><tr><td>Out of service</td><td>${mt[e.oos]?"Yes":"No"}</td></tr><tr><td>Station point</td><td>${e.t}<br>${e.h}<br>${e.c}</td></tr></table><h4>Alarm (${t.length})</h4><div class="alist">${t.map(i=>`<div class="${jn.has(i.n)?"on":""}">${i.t}</div>`).join("")}</div>`,tt("info").className="open"}var lb=tt("gallery");Tg.forEach(n=>{let e=document.createElement("button");e.textContent=br[n][0],e.title=br[n][1],e.onclick=()=>{let t=Is.find(i=>i.x===n&&(n==="airside"||i.e[0]!=="BUILDING"))||Is.find(i=>i.x===n);t&&xp(t.n)},lb.appendChild(e)});tt("asel").innerHTML='<option value="">\u2014 pick any alarm (all '+Is.length+" entries) \u2014</option>"+Tg.map(n=>`<optgroup label="${br[n][0]} / ${br[n][1]}">${Is.filter(e=>e.x===n).map(e=>`<option value="${e.n}">${e.e.join(",")} \xB7 ${e.t}</option>`).join("")}</optgroup>`).join("");tt("asel").onchange=n=>{n.target.value&&xp(n.target.value),n.target.value=""};tt("aclear").onclick=()=>{jn.clear(),Cu()};for(let n of["temp","rh","hour"])tt("w_"+n).oninput=e=>{js[n]=+e.target.value,js.on=!0,tt("wovr").checked=!0};tt("wovr").onchange=n=>js.on=n.target.checked;tt("xray").onchange=n=>{Wl.forEach(e=>{e.opacity=n.target.checked?.16:1,e.depthWrite=!n.target.checked}),Ol.opacity=n.target.checked?.14:.42,Ol.depthWrite=!1};tt("xray").onchange({target:tt("xray")});var ba={iso:[[112,84,82],[32,14,-20],"all"],plant:[[40,20,20],[20,1,-9],"1"],pumps:[[51,12,5],[37,1,-7],"1"],room:[[1.5,1.7,-13.6],[20,1.2,-10.5],"1"],roof:[[54,58,28],[26,36,-6],"all"],floor:[[70,40,40],[32,22,-20],"5"],site:[[150,110,120],[32,10,-20],"all"]};if(pi){let n=Qe.equipment.filter(o=>o.z<-1e3),e=n.reduce((o,a)=>[o[0]+a.x/n.length,o[1]+a.y/n.length],[0,0]),t=wt(e[0],e[1],ao+1200),i=n.filter(o=>o.type==="pump"),s=i.length?i.reduce((o,a)=>[o[0]+a.x/i.length,o[1]+a.y/i.length],[0,0]):e,r=wt(s[0],s[1],ao+800);ba.plant=[[t.x+14,t.y+13,t.z+16],t.toArray(),"0"],ba.pumps=[[r.x+7,r.y+7,r.z+9],r.toArray(),"0"],ba.room=[[t.x-12,t.y+1.2,t.z+4],t.toArray(),"0"]}document.querySelectorAll("[data-view]").forEach(n=>n.onclick=()=>{let[e,t,i]=ba[n.dataset.view];Qs(e,t),i&&typeof Js=="function"&&(gn=i,tt("fsel").value=i,Js())});function rg(){let n=Date.now()/1e3,e=new Date().getHours()+new Date().getMinutes()/60,t=Math.sin,i=Math.floor(n/50)%3;try{Cs&&Cs.demo(n)}catch{}let s=u=>Qe.installed[u]??!1,r=Object.keys(Qe.installed).filter(u=>/^CH\d/.test(u)&&s(u)),o=Math.min(r.length,[1,2,3][i]),a=r.slice(0,o),c=270*o+25*t(n/30);Object.assign(mt,{OA_Temperature:30+5*t(Math.PI*(e-9)/12),OA_Humidity:66-14*t(Math.PI*(e-9)/12),OA_WetBulb:26.5,CHWFlow:c*2.4+20*t(n/9),CDW_Flow:1e3*o,CHWS:6.7+.1*t(n/20),CHWR:12.1+.2*t(n/25),CDS:29.6+.3*t(n/40),CDR:34.4+.3*t(n/40),CoolingLoad_RT:c,Plant_kW:c*(.79+.03*t(n/60)),Plant_kW_per_RT:.79+.03*t(n/60),Gfx_CHW_BypassMV_Pos:o>1?6:22+10*t(n/7)});for(let u in Qe.installed)mt[u+"_Installed"]=Qe.installed[u];for(let u of Object.keys(Qe.installed).filter(d=>/^CH\d/.test(d))){let d=a.includes(u),f=+u.slice(2);Object.assign(mt,{[u+"RunProof"]:d,[u+"LoadPct"]:d?78+5*t(n/40+f):0,[u+"_ChwSupplyTemp"]:d?6.7+.1*t(n/20):12,[`Gfx_${u}_ChwIso_Pos`]:d?100:0,[`Gfx_${u}_CdwIso_Pos`]:d?100:0}),f<=2&&Object.assign(mt,{[`Gfx_${u}_ChwFCV_Pos`]:d?70+12*t(n/11):0,[`Gfx_${u}_CdwHPV_Pos`]:d?60+20*t(n/15):0})}for(let u of["CHP","CDP","CT"]){let d=Object.keys(Qe.installed).filter(f=>new RegExp("^"+u+"\\d").test(f)&&s(f)).slice(0,o);for(let f of Object.keys(Qe.installed).filter(p=>new RegExp("^"+u+"\\d").test(p))){let p=d.includes(f),x=+f.slice(-2);if(u==="CT"){if(x<=2)for(let b of["01","02"])Object.assign(mt,{[`${f}_${b}RunProof`]:p,[`${f}_${b}SpeedCmd`]:p?70:0});else Object.assign(mt,{[f+"RunProof"]:p,[f+"SpeedCmd"]:p?70:0});Object.assign(mt,x<=2?{[`Gfx_${f}_InletMV_Pos`]:p?100:0,[`Gfx_${f}_OutletMV_Pos`]:p?100:0}:{[`Gfx_${f}_Valve_Pos`]:p?100:0})}else Object.assign(mt,{[f+"RunProof"]:p,[f+"SpeedCmd"]:p?80:0},x<=2?{[`Gfx_${f}_SuctionMV_Pos`]:p?100:0,[`Gfx_${f}_DischargeMV_Pos`]:p?100:0}:{[`Gfx_${f}_MV_Pos`]:p?100:0})}}let l=e>7&&e<20;for(let u of Qe.air_equipment){let d=l||u.type==="fan"&&/EF/.test(u.id);mt[u.run]=d,u.type==="ahu"&&(mt[u.pt+"_ValveCmd"]=d?55+20*t(n/23+u.floor):0)}for(let u of Qe.zones){let d=u.floor*7+ +u.code.slice(-2);mt[u.t]=(l?24:27.5)+1.4*t(n/37+d)+(d%5===0?2.2:0),mt[u.h]=58+8*t(n/45+d),mt[u.c]=(l?720:480)+180*t(n/53+d)+(d%6===0?380:0)}}var vp=0;function cb(){ki||(ki=!0,tt("mode").textContent="DEMO \xB7 simulated data, no commands sent \xB7 1 \u2192 2 \u2192 3 chillers every 50 s",tt("mode").className="mode demo",document.body.classList.add("is-demo"),rg(),vp=setInterval(rg,1e3),tt("sim").style.display="")}function jf(){pp=!0,ki&&(clearInterval(vp),ki=!1),tt("mode").textContent="OFFLINE \xB7 no data from the station",tt("mode").className="mode offline",tt("sim").style.display="none"}var hb=/^https?:$/.test(location.protocol)&&!/[?&]demo\b/.test(location.search);function ub(n){return n?n.isDown&&n.isDown()?"OFFLINE":n.isStale&&n.isStale()?"STALE":n.isFault&&n.isFault()||n.isNull&&n.isNull()||n.isDisabled&&n.isDisabled()?"BAD":"OK":"BAD"}function db(){let n={OK:0,BAD:0,STALE:0,OFFLINE:0,UNBOUND:0};for(let e in Ma)n[as.has(e)?"UNBOUND":np[e]||"UNBOUND"]++;return n}function fb(){let n=window.BAJA_READY;if(!n||!hb)return cb();let e=!1;setTimeout(()=>{e||jf()},7e3),n.then(()=>window.require(["baja!"],function(t){e=!0,pp=!0,ki&&(clearInterval(vp),ki=!1,tt("sim").style.display="none",jn.clear()),tt("mode").textContent="LIVE \xB7 station data",tt("mode").className="mode live";let i=new t.Subscriber,s=new Map;i.attach("changed",function(g){g.getName()==="out"&&r(this)});function r(g){for(let m of s.get(g)||[])o(g,m)}function o(g,m){try{let A=g.get("out"),U=A.getValue(),T=A.getStatus();if(m.alarm){let I=m.alarm;T&&T.isAlarm&&T.isAlarm()||typeof U=="boolean"&&U===I.av?jn.set(I.n,I):jn.delete(I.n),Cu()}else{let I=ub(T);np[m.v]=I,I==="OK"?mt[m.v]=U:delete mt[m.v]}}catch{m.v&&(np[m.v]="BAD",delete mt[m.v])}}let a=[...Object.entries(Ma).map(([g,m])=>({s:m,v:g})),...Is.filter(g=>g.s).map(g=>({s:g.s,alarm:g}))],c=new Map;for(let g of a){let m="station:|slot:"+g.s;c.has(m)||c.set(m,[]),c.get(m).push(g)}let l=(g,m)=>{if(!m)return u(g);s.has(m)||s.set(m,new Set),c.get(g).forEach(A=>{s.get(m).add(A),as.delete(A.v||A.alarm.n)}),r(m)},u=g=>c.get(g).forEach(m=>as.add(m.v||m.alarm.n)),d=g=>t.Ord.make(g).get({subscriber:i}).then(m=>l(g,m),()=>u(g)),f=[...c.keys()],p=200,x=[];for(let g=0;g<f.length;g+=p){let m=f.slice(g,g+p),A;try{let U=new t.BatchResolve(m);A=Promise.resolve(U.resolve({subscriber:i})).then(()=>m.forEach((T,I)=>typeof U.isResolved!="function"||U.isResolved(I)?l(T,U.get(I)):u(T)))}catch(U){A=Promise.reject(U)}x.push(A.catch(()=>Promise.all(m.map(d))))}let b=()=>{let g=db(),m=g.BAD+g.STALE+g.OFFLINE+g.UNBOUND;tt("mode").textContent=`LIVE \xB7 OK ${g.OK} \xB7 BAD ${g.BAD} \xB7 STALE ${g.STALE} \xB7 OFFLINE ${g.OFFLINE} \xB7 UNBOUND ${g.UNBOUND}`,tt("mode").className="mode live"+(m?" warn":"")};Promise.all(x).then(()=>{b(),setInterval(b,2e3),as.size&&console.warn("3D LIVE: ORDs not resolved",[...as])})},()=>{e=!0,jf()}),()=>{e=!0,jf()})}fb();var og=new ge({color:10134443,transparent:!0,opacity:.16,depthWrite:!1,roughness:1,metalness:0,envMapIntensity:0});function ag(n,e){n.traverse(t=>{!t.isMesh||t.material===og&&e||(e?(t.userData.orig||(t.userData.orig=t.material),t.material=og,t.castShadow=!1):t.userData.orig&&(t.material=t.userData.orig,t.castShadow=!0))})}var rp=(n,e)=>mt[n+"_Installed"]===void 0?e:!!mt[n+"_Installed"];function op(){for(let n in zt){let e=zt[n];if(!e.e.slot)continue;let t=!rp(e.e.slot,e.e.installed);t!==e.ghost&&(e.ghost=t,ag(e.g,t))}for(let n in Hi){let e=Hi[n];if(!e.p.slot)continue;let t=!rp(e.p.slot,Qe.installed[e.p.slot]);t!==e.ghost&&(e.ghost=t,ag(e.g,t),e.waters.forEach(i=>i.userData.hide=t))}}var Sr={},Ta="t",yp={t:[21,29,"\xB0C",1],h:[40,80,"%RH",0],c:[400,1200,"ppm",0]};function lg(n,e,t="t"){if(e||typeof n!="number"||isNaN(n))return new ke(9080726);let[i,s]=yp[t],r=Math.max(0,Math.min(1,(n-i)/(s-i)));return new ke().setHSL(.62-.62*r,.75,.5)}for(let n of Qe.zones){let e=ls(n.floor)+60,t=2800,i=new Oe;jt.zones.add(i),Vn(n.floor,i);let s=new ge({color:2278750,transparent:!0,opacity:.16,depthWrite:!1,roughness:.9,emissive:0}),r=ne(Ce(Me(n.x1-n.x0)-.4,Me(t),Me(n.y1-n.y0)-.4),s,i,wt((n.x0+n.x1)/2,(n.y0+n.y1)/2,e+t/2));r.castShadow=!1,r.userData.zone=n.code;let o=new hr(new ol(r.geometry),new zs({color:16777215,transparent:!0,opacity:.35}));o.position.copy(r.position),i.add(o);let a=document.createElement("canvas");a.width=512,a.height=160;let c=new ci(a),l=new es(new Li({map:c,depthWrite:!1,depthTest:!1,transparent:!0}));l.scale.set(5.6,1.75,1),l.renderOrder=5,l.position.copy(wt((n.x0+n.x1)/2,(n.y0+n.y1)/2,e+t+200)),i.add(l),Sr[n.code]={z:n,g:i,mat:s,edge:o,c:a,tex:c,sp:l}}var ap=0;function lp(n){let e=performance.now();if(e-ap<800)return;ap=e;let t=Date.now()%1e3<500;for(let s in Sr){let r=Sr[s],o=r.z,a=mt[o.t],c=mt[o.h],l=mt[o.c],u=!!mt[o.oos],d=sp.has(o.code),f=mt[o[Ta]];r.sp.visible=d||gn!=="all"&&gn!=="roof"&&+gn===o.floor,r.mat.color.copy(lg(f,u,Ta)),r.mat.emissive.setHex(d&&t?6689041:0),r.mat.opacity=u?.07:.17;let p=r.c.getContext("2d");p.clearRect(0,0,512,160),p.fillStyle=d?"rgba(120,16,16,.88)":"rgba(7,17,36,.82)",p.beginPath(),p.roundRect(4,4,504,152,18),p.fill(),p.fillStyle="#9fb0c0",p.font='600 30px "Segoe UI",sans-serif',p.fillText(`${o.code} \xB7 ${o.name}`.slice(0,30),18,44),p.fillStyle="#"+lg(a,u,"t").getHexString(),p.font='700 64px "Segoe UI",sans-serif',p.fillText(u?"OOS":typeof a=="number"?a.toFixed(1)+"\xB0C":"\u2014",18,124),p.fillStyle="#e8eef4",p.font='600 36px "Segoe UI",sans-serif',p.fillText(typeof c=="number"?c.toFixed(0)+"%RH":"",250,100),p.fillStyle=typeof l=="number"&&l>1e3?"#ffb4a8":"#e8eef4",p.fillText(typeof l=="number"?l.toFixed(0)+" ppm":"",250,142),r.tex.needsUpdate=!0}let i=tt("zlegend");if(i){let[s,r,o]=yp[Ta];i.innerHTML=`<span>${s} ${o}</span><i></i><span>${r} ${o}</span>`}}var wg=[];for(let n of Qe.systems)for(let e of n.devices){let t=new Oe;jt.systems.add(t),Vn(e.floor,t),t.userData.sys=n.id;let i=ne(new Ei(.35,18,12),new ge({color:new ke(n.color),emissive:new ke(n.color),emissiveIntensity:.2}),t,wt(e.x,e.y,ls(e.floor)+e.z)),s=wu(e.tag,34,"#ffffff",null);s.position.copy(i.position).add(new y(0,.6,0)),s.scale.set(2.4,1.2,1),t.add(s),wg.push({d:e,sy:n,m:i})}function pb(n){for(let e of wg){let t=!!mt[e.d.pt];e.m.material.emissiveIntensity=t?Math.sin(n*8)>0?2.5:.3:.2,e.m.scale.setScalar(t?1.4:1)}}var gn="all",Mr=!1,cp=n=>{let e=document.querySelector(`[data-layer="${n}"]`);return!e||e.checked};function Js(){let n=!Mr||gn===(pi?"0":"1")||gn==="roof"||gn==="all",e=pi&&gn==="0";for(let t of[hp.material,up.material])t.transparent=e,t.opacity=e?.12:1,t.depthWrite=!e;jt.plant.visible=n&&cp("plant"),jt.piping.visible=n&&cp("piping");for(let t in Sr)Sr[t].sp.scale.set(Mr?8.4:5.6,Mr?2.6:1.75,1);for(let t in Tu){let i=gn==="all"||gn==="roof"||(Mr?+t==+gn:+t<=+gn);for(let s of Tu[t])s.visible=i}for(let t in Bi)Bi[t].dataset.hidden=zt[t].g.visible&&zt[t].g.parent.visible?"":"1"}function mb(){let n=tt("layers");if(!n)return;let e={shell:"Building (structure / glazing)",plant:"Chiller plant",piping:"CHW / CDW piping",air:"Air side (AHU / fans)",zones:"Legacy AirPlug zones (4 per floor)",systems:"Other systems (fire / lighting ...)",...jt.office?{office:"Rooms (colour by temp / RH / CO2)",ducts:"SA / RA / OA / EA ducts",terminals:"VAV / diffusers / sensors / meters",airflow:"Airflow in ducts (measured airflow)"}:{},...jt.devices?{devices:"Field devices (Blender) / station points"}:{}};n.innerHTML=Object.entries(e).map(([r,o])=>`<label><input type="checkbox" data-layer="${r}" checked> ${o}</label>`).join(""),n.querySelectorAll("[data-layer]").forEach(r=>r.onchange=()=>{jt[r.dataset.layer].visible=r.checked,Js()}),tt("fsel").innerHTML='<option value="all">All floors</option>'+(pi?'<option value="0">B1 plant room</option>':"")+[...Array(Ve.floors).keys()].map(r=>`<option value="${r+1}">Floor ${r+1}</option>`).join("")+'<option value="roof">Roof</option>';let t=()=>{if(Js(),gn==="all")return Qs(...ba.iso.slice(0,2));let r=gn==="roof"?zn:ls(+gn);Qs([62,Me(r)+34,22],[32,Me(r)+1.5,-20])};tt("fsel").onchange=r=>{gn=r.target.value,t()},tt("fiso")&&(tt("fiso").onchange=r=>{Mr=r.target.checked,Js()}),tt("zmetric")&&(tt("zmetric").onchange=r=>{Ta=r.target.value,ap=0});let i=r=>{let o=["all",...pi?["0"]:[],...[...Array(Ve.floors).keys()].map(c=>String(c+1)),"roof"],a=Math.max(0,Math.min(o.length-1,o.indexOf(gn)+r));gn=o[a],tt("fsel").value=gn,t()},s={navUp:()=>i(1),navDn:()=>i(-1),navIn:()=>Jf(.6),navOut:()=>Jf(1.6),navHome:()=>{gn="all",tt("fsel").value="all",Mr=!1,tt("fiso")&&(tt("fiso").checked=!1),Js(),Qs(...ba.iso.slice(0,2))}};for(let r in s)tt(r)&&(tt(r).onclick=s[r]);tt("sysl").innerHTML=Qe.systems.map(r=>`<div><b style="color:${r.color}">\u25CF</b> ${r.name_th} <i>${r.devices.length?r.devices.length+" points":"planned \xB7 add devices in the register (sheet Systems)"}</i></div>`).join("")}var Cs=j0({scene:_n,LAYER:jt,onFloor:Vn,V:mt,FAIL:as,glb:oo,isDemo:()=>ki,reapply:()=>Js()});Fn.domElement.addEventListener("dblclick",n=>{if(!Cs||!jt.devices.visible)return;let e=Fn.domElement.getBoundingClientRect();if(Gl.set((n.clientX-e.left)/e.width*2-1,-(n.clientY-e.top)/e.height*2+1),co.setFromCamera(Gl,Kn),co.intersectObjects([...Tr.children,...jt.air.children],!0).some(i=>i.object.visible))return;let t=Cs.pick(co);t&&(n.stopImmediatePropagation(),tt("info").innerHTML=Cs.info(t),tt("info").className="open")},!0);mb();window.__CAMSET=(n,e)=>Qs(n,e,10);window.__DEVS=Cs;window.__V=mt;window.__EQ=zt;window.__ZONE=Sr;window.__PIPE=Hi;var gb=Object.defineProperties({},{$:{get:()=>tt},FAIL:{get:()=>as},devicesFloor:{get:()=>Cs&&Cs.floorVis},BLD:{get:()=>Ve},DEMO:{get:()=>ki},EQ:{get:()=>zt},LAYCHK:{get:()=>cp},LAYER:{get:()=>jt},LBL:{get:()=>Bi},M:{get:()=>Qe},MAT:{get:()=>_e},MRANGE:{get:()=>yp},P3:{get:()=>wt},PIPE:{get:()=>Hi},ROOFZ:{get:()=>zn},T:{get:()=>En},V:{get:()=>mt},VALVE:{get:()=>Vl},ZONE:{get:()=>Sr},apron:{get:()=>up},box:{get:()=>Ce},camera:{get:()=>Kn},canvasTex:{get:()=>Zn},cyl:{get:()=>pt},flyTo:{get:()=>Qs},ground:{get:()=>hp},hemi:{get:()=>bu},isInst:{get:()=>rp},mesh:{get:()=>ne},mm:{get:()=>Me},mp:{get:()=>Gl},onFloor:{get:()=>Vn},ray:{get:()=>co},renderer:{get:()=>Fn},scene:{get:()=>_n},sky:{get:()=>Su},sun:{get:()=>wi},svcMat:{get:()=>kl},textSprite:{get:()=>wu},trees:{get:()=>dp},zOf:{get:()=>ls},zoomBy:{get:()=>Jf},FSEL:{get:()=>gn,set:n=>{gn=n}},ISO:{get:()=>Mr,set:n=>{Mr=n}},METRIC:{get:()=>Ta,set:n=>{Ta=n}},applyFloor:{get:()=>Js,set:n=>{Js=n}},applyWeather:{get:()=>ip,set:n=>{ip=n}},updateGhosts:{get:()=>op,set:n=>{op=n}},updateZones:{get:()=>lp,set:n=>{lp=n}}});Y0(gb);Fn.setAnimationLoop(()=>{let n=Math.min(.05,J0.getDelta()),e=J0.elapsedTime;M1(),Gn.update(),Cs&&Cs.update(e,n,{flow:!!(tt("flow")&&tt("flow").checked)});let t=Eg();ip(t,e),yr.material.opacity>0&&(yr.position.y-=n*24,yr.position.y<-20&&(yr.position.y+=20)),op(),Q1(e),ib(e,n),lp(n),pb(e),rb(),Fn.render(_n,Kn)});Cu();tt("mapBtn").onclick=()=>{if(!window.MAP&&window.MAP_SRC){let i=document.createElement("script");i.src=window.ALT_URL("alt79/"+window.MAP_SRC),i.onload=()=>tt("mapBtn").onclick(),document.head.appendChild(i);return}let n=window.MAP||[],e=i=>i===void 0?"\u2014":typeof i=="number"?i.toFixed(2):String(i);tt("info").className="open wide";let t=()=>{if(!tt("info").classList.contains("wide"))return;let i=n.filter(r=>mt[r.p]!==void 0).length,s=n.filter(r=>as.has(r.p)).length;tt("info").innerHTML=`<h3>Point mapping \xB7 ${ki?"DEMO (simulated values)":"LIVE"} \xB7 values received ${i}/${n.length} points${s?` \xB7 not resolved ${s} points`:""} \xB7 alarm ${Is.filter(r=>r.s).length} points${as.size-s>0?` (not resolved ${as.size-s})`:""}</h3><button onclick="document.getElementById('info').className=''">off</button>
    <table>${n.map(r=>`<tr><td>${r.p}</td><td class="${mt[r.p]===void 0?"no":"ok"}">${as.has(r.p)?"not resolved":e(mt[r.p])}</td><td>${r.u}</td><td style="color:#9fb0c0">station:|slot:${r.s}</td></tr>`).join("")}</table>`,setTimeout(t,1e3)};t()};})();
