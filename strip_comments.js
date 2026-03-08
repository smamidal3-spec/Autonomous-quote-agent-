const fs = require('fs');
const path = require('path');
function removeComments(str) {
    const lines = str.split('\n');
    const out = [];
    let inMultiline = false;
    for (let line of lines) {
        let trimmed = line.trim();
        if (inMultiline) {
            if (trimmed.includes('*/')) {
                inMultiline = false;
            }
            continue;
        }
        if (trimmed.startsWith('/*')) {
            if (!trimmed.includes('*/')) {
                inMultiline = true;
            }
            continue;
        }
        if (trimmed.startsWith('//')) {
            continue;
        }
        if (trimmed.length > 0) {
            out.push(line);
        }
    }
    return out.join('\n');
}
function processDirectory(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (file !== 'node_modules' && file !== '.next' && file !== '.git') {
                processDirectory(fullPath);
            }
        } else if (file.endsWith('.ts') || file.endsWith('.tsx') || file.endsWith('.js') || file.endsWith('.jsx')) {
            const content = fs.readFileSync(fullPath, 'utf8');
            const newContent = removeComments(content);
            fs.writeFileSync(fullPath, newContent, 'utf8');
        }
    }
}
processDirectory(path.join(__dirname, 'frontend'));
processDirectory(__dirname);