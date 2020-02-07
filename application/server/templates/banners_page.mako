<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>Banners</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <meta content="" name="keywords">
  <meta content="" name="description">

  <!-- Favicons -->
  <link href="img/favicon.png" rel="icon">
  <link href="img/apple-touch-icon.png" rel="apple-touch-icon">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700|Raleway:400,700&display=swap"
    rel="stylesheet">

  <!-- Flexslider CSS -->
	<link rel="stylesheet" href="${request.static_url('server:static/css/flexslider.css')}" type="text/css" media="screen" />

  <!-- Bootstrap CSS File -->
  <link rel="stylesheet" href="${request.static_url('server:static/vendor/bootstrap/css/bootstrap.min.css')}"/>

  <!-- Template Main CSS File -->
  <link rel="stylesheet" href="${request.static_url('server:static/css/style.css')}"/>
</head>

<body>
  <main id="main">
    <div class="site-section">
      <div class="container">
          <div class="col-md-12 col-lg-6 text-left text-lg-right" data-aos="fade-up" data-aos-delay="100">
            <div id="filters" class="filters">
              <a href="${request.route_url('add_banner_view')}" data-filter="*">Add new banner</a>
              % if view.request.environ.get("HTTP_COOKIE") is None:
              <a href="${request.application_url}/login">Log In</a>
              % else:
              <a href="${request.application_url}/logout">Logout</a>
              % endif
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
    <div class="container container-table">
      <div class="row vertical-center-row">
        <div class="col-lg-6 text-lg-right" data-aos="fade-up" data-aos-delay="100">
          <div class="slider">
            <div class="flexslider">
              <ul class="slides">
                % for banner in banners:
                  <li>
                    <a href="${banner.url}">
                      <img src="${banner.image_path}" />
                    </a>
                    <tr>
                    <td>${banner.title}</td>
                    <td>${banner.created_at}</td>
                    <td>${banner.updated_at}</td>
                    <td>${statuses[banner.status][1]}</td>
                    <td><a href="${request.route_url('increase_banner_position_view', id=banner.id)}">Inc</a></td>
                    <td><a href="${request.route_url('decrease_banner_position_view', id=banner.id)}">Dec</a></td>
                    <td><a href="${request.route_url('update_banner_view', id=banner.id)}">Edit</a></td>
                    <td><a href="${request.route_url('delete_banner_view', id=banner.id)}">Del</a></td>
                  </li>
                % endfor
              </ul>
            </div>
        </div>
        </div>
      </div>
    </div>
  </main>

  <!-- jQuery -->
  <script src="${request.static_url('server:static/js/jquery.min.js')}"></script>

  <!-- FlexSlider -->
  <script defer src="${request.static_url('server:static/js/jquery.flexslider.js')}"></script>

  <script type="text/javascript">
    $(function(){
      SyntaxHighlighter.all();
    });
    $(window).load(function(){
      $('.flexslider').flexslider({
        animation: "slide",
        start: function(slider){
          $('body').removeClass('loading');
        }
      });
    });
  </script>
</body>
</html>
