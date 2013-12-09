%
<form action="" method="GET">
    <center>
        <table>
            <tr>
                <th>Input/Copy LaTeX Code Here</th>
                <th>Rendered by MathJax</th>
            </tr>
            <tr>
                <td class="td_textarea">
                    % if get('query'):
                    <textarea class="textarea" name='query'>{{get('query', 'abc')}}</textarea>
                    % else:
                    <textarea class="textarea" name='query'>\frac{\pi}{4}=\cfrac{1}{1+\cfrac{1^2}{2+\cfrac{3^2}{2+\cfrac{5^2}{2+\ddots}}}}=1-\frac{1}{3}+\frac{1}{5}-\frac{1}{7}+\dots</textarea>
                    % end
                </td>
                <td class="td_formula"><div class="formula"></div></td>
            </tr>
            <tr>
                <td class="td_textarea">
                    <input class="button" type="submit" name="search" value="search"></input>
                </td>
            </tr>
        </table>
    </center>
</form>
