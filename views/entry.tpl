% if get('entry'):
<center>
<math>
{{!entry['pmml']}}
</math>
</center>
<div>[Score]: {{entry['score']}}</div>
<div>[Page]:
    <a href="http://en.wikipedia.org/wiki/{{'_'.join(entry['title'].split())}}" target="_blank">
        {{entry['title']}}
    </a>
</div>
% end
