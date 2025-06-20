import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class ImageScanner {
    static final String[] IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"};
    static List<String> imagePaths = new ArrayList<>();

    public static void main(String[] args) {
        File root = new File("D:\\");
        scanDirectory(root);

        for (String path : imagePaths) {
            System.out.println(path);
        }

        System.out.println("\nTotal number of images: " + imagePaths.size());
    }

    static void scanDirectory(File dir) {
        File[] files = dir.listFiles();
        if (files == null) return;

        for (File file : files) {
            if (file.isDirectory()) {
                scanDirectory(file);
            } else {
                String fileName = file.getName().toLowerCase();
                for (String ext : IMAGE_EXTENSIONS) {
                    if (fileName.endsWith(ext)) {
                        imagePaths.add(file.getAbsolutePath());
                        break;
                    }
                }
            }
        }
    }
}
