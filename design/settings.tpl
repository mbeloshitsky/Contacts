<form id="editForm" method="POST" action="/settings">
%for e in entries:
<div class="entry {{e.fsysname}}">
  <input type="hidden" class="fn" name="fn" value="{{e.fn}}"> 
  <input type="hidden" name="deford" value="{{e.deford}}">
  <input class="caption" name="caption" value="{{e.caption}}">
  <input class="tooltip" name="tooltip" value="{{e.tooltip}}">
  <input class="fsysname" name="fsysname" value="{{e.fsysname}}">
</div>
%end
</form>
%include design/settingsNew
%rebase design/layout title='Поля контактного справочника'
