<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>MyPortfolio</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <meta content="" name="keywords">
  <meta content="" name="description">

  <!-- Favicons -->
  <link href="img/favicon.png" rel="icon">
  <link href="img/apple-touch-icon.png" rel="apple-touch-icon">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700|Raleway:400,700&display=swap"
    rel="stylesheet">

  <!-- Bootstrap CSS File -->
  <link rel="stylesheet" href="${request.static_url('server:static/vendor/bootstrap/css/bootstrap.min.css')}"/>

  <!-- Template Main CSS File -->
  <link rel="stylesheet" href="${request.static_url('server:static/css/style.css')}"/>
</head>

<body>
  <main id="main">
    <div class="site-section site-portfolio">
      <div class="container">  <link href="" rel="stylesheet">
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
    <table class="table">
      <thead class="thead-dark">
        <tr>
            <th scope="col">#</th>
            <th scope="col">Title</th>
            <th scope="col">Image</th>
            <th scope="col">Url</th>
            <th scope="col">Visible</th>
            <th scope="col">Created at</th>
            <th scope="col">Updated at</th>
            <th scope="col">Inc</th>
            <th scope="col">Dec</th>
            <th scope="col">Edit</th>
            <th scope="col">Del</th>
        </tr>
      </thead>
      <tbody>
        % for banner in banners:
            <tr>
            <th scope="row">${banner.position}</th>
            <td>${banner.title}</td>
            <td><img src="${banner.image_path}" height=100 size=100/></td>
            <td>${banner.url}</td>
            <td>${banner.created_at}</td>
            <td>${banner.updated_at}</td>
            <td>${banner.visible}</td>
            <td><a href="${request.route_url('increase_banner_position_view', id=banner.id)}">Inc</a></td>
            <td><a href="${request.route_url('decrease_banner_position_view', id=banner.id)}">Dec</a></td>
            <td><a href="${request.route_url('update_banner_view', id=banner.id)}">Edit</a></td>
            <td><a href="${request.route_url('delete_banner_view', id=banner.id)}">Del</a></td>
        </tr>
        % endfor
      </tbody>
    </table>
  </main>
</body>
</html>
