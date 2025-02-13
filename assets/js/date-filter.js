function hideOld() {
  var hidden = 0;
  document.querySelectorAll('[data-post-date]').forEach(function(post) {
    var dateDiff = (Date.now() - Date.parse(post.getAttribute("data-post-date"))) / 86400000
    if (dateDiff > 7) {
      post.style.display = 'none';
      hidden++;
    }
  });
  if (hidden > 0) {
    document.getElementById('showall').style.display = 'inline-block'; 
  }
}

function showAll() {
  document.querySelectorAll('[data-post-date]').forEach(
    (post) => post.style.display = 'block'
  ); 
  document.getElementById('showall').style.display = 'none'; 
}
