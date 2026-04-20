use axum::{
    response::Html,
    routing::get,
    Router,
};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(index_handler));

    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    println!("Forex Dashboard Terminal running at http://127.0.0.1:8080");
    println!("Press Ctrl+C to stop the server cleanly...");
    
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("failed to install CTRL+C signal handler");
    println!("\nShutting down gracefully...");
}

async fn index_handler() -> Html<&'static str> {
    Html(include_str!("../static/index.html"))
}
