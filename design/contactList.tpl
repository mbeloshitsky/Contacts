%for e in entries:
<span class="entry" title="{{e.tooltip}}">
      <span class="c_caption">{{e.caption}}</span> 
      {{e.value}} 
</span>
%end
%rebase design/layout title='Контактный справочник'
