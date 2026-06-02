// Controls components index file
import { PageControls } from './PageControls.js';
import { LorasControls } from './LorasControls.js';
import { AnimaLorasControls } from './AnimaLorasControls.js';
import { CheckpointsControls } from './CheckpointsControls.js';
import { EmbeddingsControls } from './EmbeddingsControls.js';

// Export the classes
export { PageControls, LorasControls, AnimaLorasControls, CheckpointsControls, EmbeddingsControls };

/**
 * Factory function to create the appropriate controls based on page type
 * @param {string} pageType - The type of page ('loras', 'anima_loras', 'checkpoints', or 'embeddings')
 * @returns {PageControls} - The appropriate controls instance
 */
export function createPageControls(pageType) {
    if (pageType === 'loras') {
        return new LorasControls();
    } else if (pageType === 'anima_loras') {
        return new AnimaLorasControls();
    } else if (pageType === 'checkpoints') {
        return new CheckpointsControls();
    } else if (pageType === 'embeddings') {
        return new EmbeddingsControls();
    } else {
        console.error(`Unknown page type: ${pageType}`);
        return null;
    }
}