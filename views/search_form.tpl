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
                    <textarea class="textarea" name='query'><mi>a</mi><mo>+</mo><mi>b</mi></textarea>
                    % end
                </td>
                <td class="td_formula"><div class="formula"></div></td>
            </tr>
            <tr>
                <td class="td_textarea">
                    Language:
                    <select id="lang" name="lang">
                        <option value="pmml">(Presentation) MathML</option>
                        <option value="latex">LaTeX</option>
                    </select>
                    <input class="button" type="submit" name="search" value="search"></input>
                </td>
            </tr>
        </table>
    </center>
</form>
