
import { FaceLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22/vision_bundle.mjs";

let lm=null, running=false, raf=null, last=0;

async function ensure(){
  if(lm) return lm;
  const files = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22/wasm");
  const opts=d=>({ baseOptions:{ modelAssetPath:"https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task", delegate:d }, runningMode:"VIDEO", numFaces:1, outputFaceBlendshapes:false });
  try{ lm = await FaceLandmarker.createFromOptions(files, opts("GPU")); }
  catch(e){ lm = await FaceLandmarker.createFromOptions(files, opts("CPU")); }
  return lm;
}

function place(overlay, pts, video){
  const stage = overlay.parentElement, sr = stage.getBoundingClientRect();
  const vw=video.videoWidth, vh=video.videoHeight;
  if(!vw||!vh) return;
  const scale=Math.max(sr.width/vw, sr.height/vh);
  const dw=vw*scale, dh=vh*scale, ox=(sr.width-dw)/2, oy=(sr.height-dh)/2;
  const P=i=>({ x: ox + (1-pts[i].x)*dw, y: oy + pts[i].y*dh });   // 1-x : video is mirrored
  const top=P(10), chin=P(152), L=P(234), R=P(454), eL=P(33), eR=P(263), fL=P(54), fR=P(284);
  // head width across the temples (a bit wider than cheek width) for a natural cap
  const templeW=Math.hypot(fR.x-fL.x, fR.y-fL.y);
  const faceW=Math.max(Math.hypot(R.x-L.x, R.y-L.y), templeW);
  const faceH=Math.hypot(chin.x-top.x, chin.y-top.y);
  const roll=Math.atan2(eL.y-eR.y, eL.x-eR.x);          // radians (mirrored eyes)
  const mul=(window.__hairMul||1);
  const hairW=faceW*2.08*mul;
  const hairH=hairW*200/240;                             // svg viewBox 240x200
  // hairline point (slightly above forehead landmark 10), centred on forehead
  const hlX=top.x, hlY=top.y - faceH*0.03;
  // in the svg the hairline sits at y=98/200 = 0.49 of the box height → align it there
  overlay.style.width=hairW+'px';
  overlay.style.height=hairH+'px';
  overlay.style.left=(hlX-hairW/2)+'px';
  overlay.style.top=(hlY-hairH*0.49)+'px';
  overlay.style.transformOrigin='50% 49%';              // pivot at the hairline
  overlay.style.transform='rotate('+(roll*180/Math.PI)+'deg)';
}

window.startGrizzlyCam = async function(video, overlay, onReady, onError){
  try{
    const engine = await ensure();
    running=true; if(onReady) onReady();
    const loop=()=>{
      if(!running) return;
      try{
        if(video.readyState>=2 && video.videoWidth){
          const t=performance.now();
          const res = engine.detectForVideo(video, t);
          if(res && res.faceLandmarks && res.faceLandmarks[0]){
            place(overlay, res.faceLandmarks[0], video);
            overlay.style.opacity='1';
          } else { overlay.style.opacity='.12'; }
        }
      }catch(e){}
      raf=requestAnimationFrame(loop);
    };
    loop();
    return true;
  }catch(e){ if(onError) onError(e); return false; }
};
window.stopGrizzlyCam = function(){ running=false; if(raf) cancelAnimationFrame(raf); };
window.__grizzlyARready = true;
