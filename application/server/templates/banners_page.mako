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
              <a href="${request.route_url('add_banner_view')}" data-filter="*" class="active">Add new banner</a>
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
          <th scope="col">Image path</th>
          <th scope="col">Url</th>
          <th scope="col">Status</th>
        </tr>
      </thead>
      <tbody>
        % for banner in banners:
          <tr>
          <th scope="row">${banner.position}</th>
          <td>${banner.title}</td>
          <td>${banner.image_path}</td>
          <td>${banner.url}</td>
          <td>${banner.status}</td>
        </tr>
        % endfor
      </tbody>
    </table>
  </main>
</body>
</html>