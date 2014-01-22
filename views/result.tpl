% if 'offset' in res:
% if 'count' in res:
<center>
    % if res.get('previous'):
        <a href="?{{res['previous']}}">Previous Page</a>
    % else:
        <font color="gray">Previous Page</font>
    % end
    |<a href="?{{res.get('next')}}">Next Page</a>
</center>
% end
% end
% if res.get('time'):
<div class="time"> Time Used: {{res['time']}}</div>
% end
% if res.get('entry_list'):
    <div class="entry_list">
        % for i in xrange(len(res['entry_list'])):
            % if i % 2 == 0:
            <div class="entry even">
            % else:
            <div class="entry odd">
            % end
            % include entry entry=res['entry_list'][i]
            </div>
        % end
    </div>
% else:
    <div class="msg">
        None result found.
        <br>
        Please input a more complex query.
    </div>
% end
% if res.get('error'):
<div class="msg"> Error: {{res['error']}}</div>
% end
% rebase base query=get('query', ''), lang=get('lang', 'latex')
