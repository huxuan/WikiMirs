<html>
    <link rel="stylesheet" href="style.css" />
    <head>
        <title>WikiMirs</title>
        <script type="text/javascript" src="MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
        <script type="text/javascript" src="jquery-1.8.3.min.js"></script>
        <script>
            $(function () {
                var txt = $('textarea'),
                    formulaDiv = $('div.formula'),
                    hiddenDiv = $(document.createElement('div')),
                    content = txt.val();

                $('body').append(hiddenDiv);
                txt.addClass('txtstuff');
                hiddenDiv.addClass('hiddendiv textarea');

                formulaDiv.html('\\[' + content + '\\]');
                MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
                content = content.replace(/\n/g, '<br>');
                hiddenDiv.html(content + '<br>');
                txt.css('height', hiddenDiv.height());

                txt.on('keyup', function () {

                    content = $(this).val();

                    formulaDiv.html('\\[' + content + '\\]');
                    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);

                    content = content.replace(/\n/g, '<br>');
                    hiddenDiv.html(content + '<br>');

                    $(this).css('height', hiddenDiv.height());

                });

            });
        </script>
    </head>
    <body>
        <div class="title">
            <center>
                % if get('show_title'):
                <h1> Welcome to <a href="">WikiMirs</a>!</h1>
                <h2>
                    Another way to search mathematical formula on
                    <a href="http://www.wikipedia.org/" target="_blank">
                        Wikipedia
                    </a>
                    by LaTeX
                </h2>
                % else:
                <h2><a href="">WikiMirs</a></h2>
                % end
            </center>
        </div>
        % include search_form query=get('query', '')
        % include
    </body>
</html>
