"""
PWA Setup Utilities for NexSupply
Handles Progressive Web App configuration and service worker registration.
"""
import streamlit as st


def register_service_worker():
    """Register service worker for PWA functionality."""
    service_worker_script = """
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(function(registration) {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(function(err) {
                        console.log('ServiceWorker registration failed: ', err);
                    });
            });
        }
    </script>
    """
    st.markdown(service_worker_script, unsafe_allow_html=True)


def add_pwa_meta_tags():
    """Add PWA meta tags to HTML head."""
    pwa_meta = """
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0EA5E9">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="NexSupply">
    <meta name="description" content="AI-powered B2B sourcing intelligence platform">
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/icon-192.png">
    <link rel="apple-touch-icon" sizes="192x192" href="/icon-192.png">
    <link rel="apple-touch-icon" sizes="512x512" href="/icon-512.png">
    """
    st.markdown(pwa_meta, unsafe_allow_html=True)




