<%inherit file="base_page.mako"/>

<%block name="title">
    Banners
</%block>

<%block name="css">
    <!-- Flexslider CSS -->
	<link rel="stylesheet" href="${request.static_url('server:static/css/flexslider.css')}" type="text/css" media="screen" />
</%block>



<%block name="main">
    <div class="site-section">
      <div class="container">
            <div class="col-md-12 col-lg-6 text-left text-lg-right" data-aos="fade-up" data-aos-delay="100">
                <div id="filters" class="filters">
                    % if user is None:
                    <a href="${request.route_url('login_view')}">Log In</a>
                    % else:
                    <a href="${request.route_url('logout_view')}">Logout</a>
                    % endif
                    % if user and "group:admin" in user.groups():
                    <a href="${request.route_url('admin_view')}">Admin page</a>
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
                  </li>
                % endfor
              </ul>
            </div>
        </div>
        </div>
      </div>
    </div>
</%block>

<%block name="js">
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
</%block>