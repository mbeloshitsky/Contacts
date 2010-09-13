%for ent in entries:
<div class="entry">
  %for f,v in ent.items():
  <span class="entry {{f}}" title="">
    <span class="caption">{{f}}</span>
    {{v}} 
  </span>
  %end
</div>
%end
%rebase design/layout title='Контактный справочник'
