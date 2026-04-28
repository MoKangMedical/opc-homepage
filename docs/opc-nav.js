/* MoKangMedical OPC Ecosystem Navigation Widget v2.0 */
(function(){
  var PROJECTS = [
    {name:"OPC创业者联盟",url:"https://mokangmedical.github.io/opc-homepage/",cat:"core"},
    {name:"OPC Platform",url:"https://mokangmedical.github.io/opc-platform/",cat:"core"},
    {name:"OPC Marketplace",url:"https://mokangmedical.github.io/opc-marketplace/",cat:"core"},
    {name:"天眼 Tianyan",url:"https://mokangmedical.github.io/tianyan/",cat:"med"},
    {name:"PharmaSim",url:"https://mokangmedical.github.io/PharmaSim/",cat:"med"},
    {name:"MediChat-RD",url:"https://mokangmedical.github.io/medichat-rd/",cat:"med"},
    {name:"慢康智枢",url:"https://mokangmedical.github.io/chronicdiseasemanagement/",cat:"med"},
    {name:"MedRoundTable",url:"https://mokangmedical.github.io/medroundtable/",cat:"med"},
    {name:"VoiceHealth",url:"https://mokangmedical.github.io/voicehealth/",cat:"med"},
    {name:"HealthGuard OPC",url:"https://mokangmedical.github.io/healthguard-opc/",cat:"med"},
    {name:"Virtual Cell",url:"https://mokangmedical.github.io/virtual-cell/",cat:"sci"},
    {name:"NHANES-to-Lancet",url:"https://mokangmedical.github.io/nhanes-to-lancet/",cat:"sci"},
    {name:"HEOR Modeling",url:"https://mokangmedical.github.io/heor-modeling-platform/",cat:"sci"},
    {name:"康波研究院",url:"https://mokangmedical.github.io/kondratiev-wave/",cat:"edu"},
    {name:"Digital Sage",url:"https://mokangmedical.github.io/digital-sage/",cat:"edu"},
    {name:"Cloud Memorial",url:"https://mokangmedical.github.io/cloud-memorial/",cat:"life"},
    {name:"NarrowGate",url:"https://mokangmedical.github.io/narrowgate/",cat:"life"}
  ];
  var CATS = {core:"核心平台",med:"医疗AI",sci:"科研工具",edu:"知识教育",life:"生活传承"};
  var current = location.href.replace(/\/index\.html$/,'/').replace(/\/$/,'');

  /* Styles */
  var css = document.createElement('style');
  css.textContent = `
#opc-nav-btn{position:fixed;bottom:24px;right:24px;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;font-size:22px;font-weight:700;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:9999;box-shadow:0 4px 20px rgba(99,102,241,.4);transition:all .3s;border:none;font-family:Inter,system-ui,sans-serif}
#opc-nav-btn:hover{transform:scale(1.1);box-shadow:0 6px 28px rgba(99,102,241,.5)}
#opc-nav-panel{position:fixed;bottom:90px;right:24px;width:320px;max-height:480px;background:#111827;border:1px solid #374151;border-radius:16px;z-index:9999;display:none;overflow:hidden;font-family:Inter,system-ui,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.5)}
#opc-nav-panel.open{display:block;animation:opcSlideUp .3s ease}
@keyframes opcSlideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
#opc-nav-panel .opc-header{padding:16px 20px;background:linear-gradient(135deg,#1e1b4b,#312e81);display:flex;align-items:center;justify-content:space-between}
#opc-nav-panel .opc-header span{color:#e0e7ff;font-size:14px;font-weight:600}
#opc-nav-panel .opc-close{background:none;border:none;color:#a5b4fc;cursor:pointer;font-size:18px;padding:4px}
#opc-nav-panel .opc-body{overflow-y:auto;max-height:400px;padding:8px 0}
#opc-nav-panel .opc-cat{padding:8px 20px 4px;font-size:11px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:.5px}
#opc-nav-panel .opc-link{display:flex;align-items:center;padding:10px 20px;color:#d1d5db;font-size:13px;text-decoration:none;transition:all .15s;gap:10px}
#opc-nav-panel .opc-link:hover{background:#1f2937;color:#fff}
#opc-nav-panel .opc-link.current{background:#1e1b4b;color:#a5b4fc;border-left:3px solid #6366f1}
#opc-nav-panel .opc-link .opc-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
#opc-nav-panel .opc-footer{padding:12px 20px;border-top:1px solid #1f2937;text-align:center}
#opc-nav-panel .opc-footer a{color:#6b7280;font-size:11px;text-decoration:none}
#opc-nav-panel .opc-footer a:hover{color:#a5b4fc}
`;
  document.head.appendChild(css);

  /* Button */
  var btn = document.createElement('button');
  btn.id = 'opc-nav-btn';
  btn.innerHTML = 'M';
  btn.title = 'MoKangMedical Ecosystem';
  btn.onclick = function(){panel.classList.toggle('open')};
  document.body.appendChild(btn);

  /* Panel */
  var panel = document.createElement('div');
  panel.id = 'opc-nav-panel';
  var html = '<div class="opc-header"><span>MoKangMedical 17 Projects</span><button class="opc-close" onclick="this.closest(\'#opc-nav-panel\').classList.remove(\'open\')">&times;</button></div><div class="opc-body">';

  var lastCat = '';
  PROJECTS.forEach(function(p){
    if(p.cat !== lastCat){
      html += '<div class="opc-cat">' + CATS[p.cat] + '</div>';
      lastCat = p.cat;
    }
    var isCurrent = current === p.url.replace(/\/$/,'');
    html += '<a class="opc-link' + (isCurrent?' current':'') + '" href="' + p.url + '"><span class="opc-dot" style="background:' + (isCurrent?'#6366f1':'#374151') + '"></span>' + p.name + '</a>';
  });

  html += '</div><div class="opc-footer"><a href="https://github.com/MoKangMedical">github.com/MoKangMedical</a></div>';
  panel.innerHTML = html;
  document.body.appendChild(panel);

  /* Close on outside click */
  document.addEventListener('click', function(e){
    if(!panel.contains(e.target) && e.target !== btn) panel.classList.remove('open');
  });
})();
