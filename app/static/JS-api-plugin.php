<?php
/**
Plugin Name: iFrame scrol and resize
*/
add_action( 'wp_head', 'add_js_scripts' );
function add_js_scripts(){
  ?>
  <script>console.log('iFrame scrol and resize added'); </script>
  <script src="https://api.molssi.org/static/js/wordpress_parent.js" type="text/javascript"></script>
  <?php
  // <script src="http://localhost:5000/static/js/wordpress_parent.js" type="text/javascript"></script>
}