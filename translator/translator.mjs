import { pipeline, env } from '@xenova/transformers';
import readline from 'readline';

// Set the cache directory from the command-line arguments
const customPath = process.argv[3];
if (customPath) {
    env.cacheDir = customPath;
}

// Create a singleton wrapper for the translation pipeline
class Translator {
    static instance = null;

    static async getInstance(model) {
        if (this.instance === null) {
            this.instance = await pipeline('translation', model);
        }
        return this.instance;
    }
}

// The main function to run the translation
async function run() {
    // The model name is passed as a command-line argument
    const model = process.argv[2];
    if (!model) {
        process.stderr.write('Error: Model name not provided.\n');
        process.exit(1);
    }

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        terminal: false
    });

    for await (const line of rl) {
        if (line.trim()) {
            try {
                const translator = await Translator.getInstance(model);
                const [result] = await translator(line);
                // Use a unique delimiter to signal the end of a translation
                process.stdout.write(result.translation_text + '\n---END_OF_TRANSLATION---\n');
            } catch (e) {
                process.stderr.write(`Translation Error: ${e.message}\n---END_OF_TRANSLATION---\n`);
            }
        } else {
            // For empty lines, output an empty line and the delimiter
            process.stdout.write('\n---END_OF_TRANSLATION---\n');
        }
    }
}

run();