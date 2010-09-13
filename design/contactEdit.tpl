<form method="POST" action="/edit">
%if entry['_id'] == 'new':
    %title = 'Создать контакт'
%else:
    %title = 'Редактировать контакт'
%end
%for f,v in entry.items():
  <p><strong>{{f}}</strong>:<input name="{{f}}" value="{{v}}"></p>
%end
<p><input type="submit" value="Отправить"></p>
</form>
%rebase design/layout title="Редактировать контакт"
