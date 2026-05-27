const API_URL = 'http://5.42.113.201:8888/api'; 

async function handleResponse(response) {
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || `HTTP ${response.status}`);
    }
    return response.json();
}

export const api = {
    getContentPages: () => fetch(`${API_URL}/content-pages`).then(handleResponse),
    getPage: (id) => fetch(`${API_URL}/content-pages/${id}`).then(handleResponse),
    getBanners: () => fetch(`${API_URL}/banners`).then(handleResponse),
    getCategories: () => fetch(`${API_URL}/service-categories`).then(handleResponse),
    getServices: () => fetch(`${API_URL}/services`).then(handleResponse),
    getService: (id) => fetch(`${API_URL}/services/${id}`).then(handleResponse),
    getServicesByCategory: (id) => fetch(`${API_URL}/services/by-category/${id}`).then(handleResponse),
    // getPrices: () => fetch(`${API_URL}/prices`).then(handleResponse),  // УДАЛЕНО - цена теперь в услуге
    // getPricesByService: (id) => fetch(`${API_URL}/prices/by-service/${id}`).then(handleResponse),  // УДАЛЕНО
    getContacts: () => fetch(`${API_URL}/contacts`).then(handleResponse),
    getSeo: (pageId) => fetch(`${API_URL}/seo/${pageId}`).then(handleResponse),
    sendRequest: (data) => fetch(`${API_URL}/requests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(handleResponse)
};
