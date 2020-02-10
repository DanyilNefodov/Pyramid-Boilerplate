<%inherit file="base_page.mako"/>

<%block name="title">
    Admin page
</%block>

<%block name="main">
    <div class="site-section site-portfolio">
        <div class="container">  <link href="" rel="stylesheet">
            <div class="col-md-12 col-lg-6 text-left text-lg-right" data-aos="fade-up" data-aos-delay="100">
                <div id="filters" class="filters">
                    <a>
                        <form id="csrf_input" method="post" action="${request.route_url('banners_view')}">
                            <input type="submit" value="Home Page">
                        </form>
                    </a>
                    <a>
                        <form id="csrf_input" method="post" action="${request.route_url('add_banner_view')}">
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input type="submit" value="Add New Banner">
                        </form>
                    </a>

                    <a>
                        % if user is None:
                            <form method="post" action="${request.route_url('login_view')}">
                                <input type="submit" value="Log In">
                            </form>
                        % else:
                            <form method="post" action="${request.route_url('logout_view')}">
                                <input type="submit" value="Log Out">
                            </form>
                        % endif
                    </a>
                </div>
            </div>
        </div>
    </div>
    ${form | n}
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
                    <td>${banner.visible}</td>
                    <td>${banner.created_at}</td>
                    <td>${banner.updated_at}</td>
                    <td>
                        <form id="csrf_input" method="post" action="${request.route_url('increase_banner_position_view', id=banner.id)}">
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input type="submit" value="Inc">
                        </form>
                    </td>
                    <td>
                        <form id="csrf_input" method="post" action="${request.route_url('decrease_banner_position_view', id=banner.id)}">
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input type="submit" value="Dec">
                        </form>
                    </td>
                    <td>
                        <form id="csrf_input" method="post" action="${request.route_url('update_banner_view', id=banner.id)}">
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input type="submit" value="Upd">
                        </form>
                    </td>
                    <td>
                        <form id="csrf_input" method="post" action="${request.route_url('delete_banner_view', id=banner.id)}">
                            <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                            <input type="submit" value="Del">
                        </form>
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
    % if page.get("count", 0) not in (0, 1):
    <div class="container">  <link href="" rel="stylesheet">
        <div class="col-md-12 col-lg-6 text-left text-lg-right" data-aos="fade-up" data-aos-delay="100">
            <% page_count = page.get("count", 0) %>
            <div id="filters" class="filters">
                <a>
                    <form method="post" action="${request.route_url('admin_view')}">
                        <input type="submit" value="1">
                    </form>
                </a>
                % for paginator in range(2, page_count):
                    <a>
                        <form method="post" action="${request.route_url('admin_paginated_view', id=paginator)}">
                            <input type="submit" value="${paginator}">
                        </form>
                    </a>
                % endfor
                <a>
                    <form method="post" action="${request.route_url('admin_paginated_view', id=page_count)}">
                        <input type="submit" value="${page_count}">
                    </form>
                </a>
            </div>
        </div>
    </div>
    % endif
</%block>

<%block name="js">
    <script type="text/javascript">
        $(document).ready(function(){
            $('#csrf_input').on('click', function(){
                var csrfToken = "${get_csrf_token()}";
                $.ajax({
                    type: "POST",
                    url: $(this).attr('action'),
                    headers: { 'X-CSRF-Token': csrfToken }
                }));
            })
        })
    </script>
</%block>