package ro.cobrabm.fexdroid;

import android.util.Log;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Shared SotC INI persistence. Never rewrite unrelated settings or game files. */
final class SotcSettingsStore {
    private SotcSettingsStore() {}

    static boolean write(File ini, Map<String,String> updates) {
        if (updates.isEmpty()) return true;
        Path temporary=null;
        try {
            File parent=ini.getParentFile();
            if (parent==null || (!parent.isDirectory() && !parent.mkdirs()))
                throw new IOException("Missing SotC settings directory");
            List<String> original=ini.isFile()
                ? Files.readAllLines(ini.toPath(),StandardCharsets.UTF_8) : new ArrayList<>();
            List<String> output=new ArrayList<>();
            for (String line : original) {
                boolean replaced=false;
                for (String key : updates.keySet()) {
                    if (line.startsWith(key+"=")) { replaced=true; break; }
                }
                if (!replaced) output.add(line);
            }
            for (Map.Entry<String,String> e : updates.entrySet()) {
                if (!e.getKey().matches("[a-zA-Z0-9_]+") ||
                    !e.getValue().matches("[a-zA-Z0-9_]+"))
                    throw new IOException("Invalid SotC INI value for "+e.getKey());
                output.add(e.getKey()+"="+e.getValue());
            }
            temporary=Files.createTempFile(parent.toPath(),".sotc-settings-", ".ini");
            Files.write(temporary,output,StandardCharsets.UTF_8);
            try {
                Files.move(temporary,ini.toPath(),StandardCopyOption.ATOMIC_MOVE,
                    StandardCopyOption.REPLACE_EXISTING);
            } catch (AtomicMoveNotSupportedException notSupported) {
                Files.move(temporary,ini.toPath(),StandardCopyOption.REPLACE_EXISTING);
            }
            return true;
        } catch (Exception e) {
            Log.e("SotC", "Could not save runtime settings", e);
            if (temporary!=null) try { Files.deleteIfExists(temporary); } catch (IOException ignored) {}
            return false;
        }
    }
}
