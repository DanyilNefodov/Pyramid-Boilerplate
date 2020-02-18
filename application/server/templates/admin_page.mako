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
    <input type='hidden' id='sort' render-url="${request.application_url}">
    <table id='empTable' class="table">
        <thead class="thead-dark">
                <tr>
                    <th scope="col"><span onclick='sortTable("position");'>#</span></th>
                    <th scope="col"><span onclick='sortTable("title");'>Title</span></th>
                    <th scope="col">Image</th>
                    <th scope="col"><span onclick='sortTable("url");'>Url</span></th>
                    <th scope="col"><span onclick='sortTable("visible");'>Visible</span></th>
                    <th scope="col"><span onclick='sortTable("created_at");'>Created at</span></th>
                    <th scope="col"><span onclick='sortTable("updated_at");'>Updated at</span></th>
                    <th scope="col">Inc</th>
                    <th scope="col">Dec</th>
                    <th scope="col">Upd</th>
                    <th scope="col">Del</th>
                </tr>
            <input>
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
    % if page.get("count", 0) != 0:
    <div class="container">  <link href="" rel="stylesheet">
        <div class="col-md-12 col-lg-6 text-left text-lg-right" data-aos="fade-up" data-aos-delay="100">
            <% page_count = page.get("count", 0) %>
            <div id="filters" class="filters">
                <a>
                    <form method="post" action="${request.route_url('admin_view')}">
                        <input type="submit" value="1">
                    </form>
                </a>
                % if page_count > 7:
                    <% 
                        page_number = page.get("page", 7)

                        page_lower = page_number - 1
                        page_upper = page_number + 2

                        if page_lower <= 1:
                            page_lower = 2

                        if page_upper > page_count:
                            page_upper = page_count
                    %>
                    % if page_lower != 2:
                        <a>
                            ...
                        </a>
                    % endif
                    % for paginator in range(page_lower, page_upper):
                        <a>
                            <form method="post" action="${request.route_url('admin_paginated_view', id=paginator)}">
                                <input type="submit" value="${paginator}">
                            </form>
                        </a>
                    % endfor
                    % if page_upper < page_count:
                    <a>
                        ...
                    </a>
                    % endif
                % else:
                    % for paginator in range(2, page_count):
                        <a>
                            <form method="post" action="${request.route_url('admin_paginated_view', id=paginator)}">
                                <input type="submit" value="${paginator}">
                            </form>
                        </a>
                    % endfor
                % endif
                <a>
                    <form method="post" action="${request.route_url('admin_paginated_view', id=page_count)}">
                        <input type="submit" value="${page_count}">
                    </form>
                    ## <form method="post" action="${request.route_url('admin_paginated_view', id=page_count}">
                    ##     <input type="submit" value="${page_count}">
                    ## </form>
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
    <script>
    function sortTable(columnName){
        var sort = $("#sort").val();
        $.ajax({
                url: $("#sort").attr("render-url") + "/admin/sort/" + columnName,
                type:'POST'
            });
        }
    </script>
</%block>