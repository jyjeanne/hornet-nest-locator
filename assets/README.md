# Assets Folder

This folder contains static assets used by the Hornet Nest Locator application.

## Files

### `icon.ico`
- **Purpose**: Application icon for Windows executable
- **Format**: ICO (Windows Icon format)
- **Size**: 32x32 pixels
- **Design**: Yellow and black striped pattern (bee/hornet theme)
- **Usage**: Used by PyInstaller to create the standalone executable icon

## Usage

The assets in this folder are automatically included in the Windows build process via the GitHub Actions workflow. The icon is embedded in the final executable file.

## Customization

To customize the application icon:
1. Replace `icon.ico` with your own 32x32 pixel ICO file
2. Ensure the file maintains the `.ico` extension
3. The build system will automatically use the new icon

## Notes

- The icon should be simple and recognizable at small sizes
- For best results, use a design that represents the application's purpose
- Multiple icon sizes can be included in a single ICO file for better compatibility