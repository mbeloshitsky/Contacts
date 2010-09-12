<form method="POST" action="/edit">
%for f in entriy:
<span class="entry" title="{{f.tooltip}}">
  %if f._id == 'new': 
  %   title = 'Новый контакт'
  %else:
  %   title = 'Редактировать контакт'
  %end
  <input type="hidden" name="cid" value="{{f.cid}}">
  <input type="hidden" name="fkey" value="{{f.fkey}}">
  <input name="value" value="{{f.fvalue}}">
</span>
%end
<input type="submit" value="Отправить">
</form>
%rebase design/layout title=title
