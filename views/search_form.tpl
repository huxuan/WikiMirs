%
<form action="" method="GET">
    <center>
        <table>
            <tr>
                <th>Input/Copy MathML/LaTeX Code Here</th>
                <th>Rendered by MathJax</th>
            </tr>
            <tr>
                <td class="td_textarea">
                    % if get('query'):
                    <textarea class="textarea" name='query'>{{get('query', '')}}</textarea>
                    % else:
                    <textarea class="textarea" name='query'>x^n+y^n=z^n</textarea>
                    % end
                </td>
                <td class="td_formula"><div class="formula"></div></td>
            </tr>
            <tr>
                <td class="td_textarea">
                    Language:
                    <select id="lang" name="lang">
                        % if get('lang') == 'pmml':
                        <option value="pmml" selected="selected">(Presentation) MathML</option>
                        % else:
                        <option value="pmml">(Presentation) MathML</option>
                        % end
                        % if get('lang') == 'latex':
                        <option value="latex" selected="selected">LaTeX</option>
                        % else:
                        <option value="latex">LaTeX</option>
                        % end
                    </select>
                    <input class="button" type="submit" name="search" value="search"></input>
                </td>
            </tr>
        </table>
    </center>
</form>
