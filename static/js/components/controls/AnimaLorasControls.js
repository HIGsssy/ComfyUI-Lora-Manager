// AnimaLorasControls.js - Specific implementation for the Anima LoRAs page
import { PageControls } from './PageControls.js';
import { getModelApiClient, resetAndReload } from '../../api/modelApiFactory.js';
import { showToast } from '../../utils/uiHelpers.js';
import { downloadManager } from '../../managers/DownloadManager.js';

/**
 * AnimaLorasControls class - Extends PageControls for Anima LoRA functionality.
 * Mirrors the LoRA page behavior but operates on the distinct 'anima_loras' page.
 */
export class AnimaLorasControls extends PageControls {
    constructor() {
        // Initialize with 'anima_loras' page type
        super('anima_loras');

        // Register API methods specific to the Anima LoRAs page
        this.registerAnimaLorasAPI();
    }

    /**
     * Register Anima LoRA-specific API methods
     */
    registerAnimaLorasAPI() {
        const animaLorasAPI = {
            // Core API functions
            loadMoreModels: async (resetPage = false, updateFolders = false) => {
                return await getModelApiClient().loadMoreWithVirtualScroll(resetPage, updateFolders);
            },

            resetAndReload: async (updateFolders = false) => {
                return await resetAndReload(updateFolders);
            },

            refreshModels: async (fullRebuild = false) => {
                return await getModelApiClient().refreshModels(fullRebuild);
            },

            // Fetch from Civitai (hash-based, same as LoRAs)
            fetchFromCivitai: async () => {
                return await getModelApiClient().fetchCivitaiMetadata();
            },

            showDownloadModal: () => {
                downloadManager.showDownloadModal();
            },

            toggleBulkMode: () => {
                if (window.bulkManager) {
                    window.bulkManager.toggleBulkMode();
                } else {
                    console.error('Bulk manager not available');
                }
            },

            // Custom filters are only used for the regular LoRAs page
            clearCustomFilter: async () => {
                showToast('toast.filters.noCustomFilterToClear', {}, 'info');
            }
        };

        // Register the API
        this.registerAPI(animaLorasAPI);
    }
}
