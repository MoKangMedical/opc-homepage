/**
 * OPC Ecosystem Navigation Component
 * Injects a floating navigation bar at the top of any page
 * that links to all OPC projects.
 * 
 * Usage: <script src="https://mokangmedical.github.io/opc-homepage/docs/opc-nav.js"></script>
 */
(function(){
  'use strict';
  
  const PROJECTS = [
    {name:'OPC首页', url:'https://mokangmedical.github.io/opc-homepage/', icon:'O'},
    {name:'天眼', url:'https://mokangmedical.github.io/tianyan/', icon:'◉'},
    {name:'慢康智枢', url:'https://mokangmedical.github.io/chronicdiseasemanagement/', icon:'❤'},
    {name:'康波', url:'https://mokangmedical.github.io/kondratiev-wave/', icon:'📈'},
    {name:'HEOR', url:'https://mokangmedical.github.io/heor-modeling-platform/', icon:'📊'},
    {name:'MetaForge', url:'https://mokangmedical.github.io/metaforge/', icon:'🔬'},
    {name:'MediChat', url:'https://mokangmedical.github.io/medichat-rd/', icon:'💊'},
    {name:'NHANES', url:'https://mokangmedical.github.io/nhanes-to-lancet/', icon:'📋'},
    {name:'Biostats', url:'https://mokangmedical.github.io/biostats-/', icon:'🧮'},
    {name:'念念', url:'https://mokangmedical.github.io/cloud-memorial/', icon:'🕊'},
    {name:'PharmaSim', url:'https://mokangmedical.github.io/PharmaSim/', icon:'💊'},
    {name:'RoundTable', url:'https://mokangmedical.github.io/medroundtable/', icon:'🏥'},
  ];
  
  // Don't show on the homepage itself
  if(window.location.href.includes('opc-homepage')) return;
  
  // Create styles
  const style = document.createElement('style');
  style.textContent = `
    .opc-eco-nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(9,9,11,.95);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(99,102,241,.1);transform:translateY(-100%);transition:transform .3s ease}
    .opc-eco-nav.show{transform:translateY(0)}
    .opc-eco-nav-inner{max-width:1200px;margin:0 auto;padding:0 16px;height:36px;display:flex;align-items:center;gap:8px;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
    .opc-eco-nav-inner::-webkit-scrollbar{display:none}
    .opc-eco-nav-home{font-size:11px;font-weight:700;color:#6366f1;white-space:nowrap;padding:4px 10px;border-radius:6px;background:rgba(99,102,241,.1);transition:all .2s;flex-shrink:0}
    .opc-eco-nav-home:hover{background:rgba(99,102,241,.2);color:#818cf8}
    .opc-eco-nav-sep{width:1px;height:16px;background:rgba(255,255,255,.08);flex-shrink:0}
    .opc-eco-nav-link{font-size:11px;color:#a1a1aa;white-space:nowrap;padding:4px 8px;border-radius:4px;transition:all .2s;flex-shrink:0}
    .opc-eco-nav-link:hover{color:#fafafa;background:rgba(255,255,255,.06)}
    .opc-eco-nav-link.current{color:#6366f1;background:rgba(99,102,241,.08)}
    .opc-eco-nav-toggle{position:fixed;top:8px;right:12px;z-index:10000;width:28px;height:28px;border-radius:6px;background:rgba(9,9,11,.9);border:1px solid rgba(99,102,241,.2);color:#6366f1;font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s}
    .opc-eco-nav-toggle:hover{background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.4)}
    @media(max-width:640px){.opc-eco-nav-inner{padding:0 8px}}
  `;
  document.head.appendChild(style);
  
  // Create nav
  const nav = document.createElement('div');
  nav.className = 'opc-eco-nav';
  
  let html = '<div class="opc-eco-nav-inner">';
  html += '<a href="https://mokangmedical.github.io/opc-homepage/" class="opc-eco-nav-home">OPC</a>';
  html += '<div class="opc-eco-nav-sep"></div>';
  
  PROJECTS.forEach(p => {
    const isCurrent = window.location.href.includes(p.url.replace('https://mokangmedical.github.io/','').replace('/',''));
    html += `<a href="${p.url}" class="opc-eco-nav-link${isCurrent?' current':''}" target="_blank">${p.icon} ${p.name}</a>`;
  });
  
  html += '</div>';
  nav.innerHTML = html;
  document.body.appendChild(nav);
  
  // Create toggle button
  const toggle = document.createElement('button');
  toggle.className = 'opc-eco-nav-toggle';
  toggle.innerHTML = '☰';
  toggle.title = 'OPC生态导航';
  document.body.appendChild(toggle);
  
  // Show nav after 1s
  let navVisible = false;
  setTimeout(() => {
    nav.classList.add('show');
    navVisible = true;
  }, 1000);
  
  // Toggle on click
  toggle.addEventListener('click', () => {
    navVisible = !navVisible;
    nav.classList.toggle('show', navVisible);
  });
  
  // Hide on scroll down, show on scroll up
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const current = window.scrollY;
    if(current > lastScroll && current > 100) {
      nav.classList.remove('show');
    } else if(current < lastScroll) {
      nav.classList.add('show');
    }
    lastScroll = current;
  }, {passive:true});
})();
