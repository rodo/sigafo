select relname,tgname,tgtype,tgconstrrelid from pg_trigger,pg_class where pg_class.oid=pg_trigger.tgrelid order by tgname;
