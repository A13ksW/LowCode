import requests
import pandas as pd
import streamlit as st

API_BASE = "https://jsonplaceholder.typicode.com"


@st.cache_data
def fetch_data():
    """Pobiera dane z kilku endpointów JSONPlaceholder i zwraca jako DataFrame'y."""
    users = requests.get(f"{API_BASE}/users").json()
    posts = requests.get(f"{API_BASE}/posts").json()
    comments = requests.get(f"{API_BASE}/comments").json()
    todos = requests.get(f"{API_BASE}/todos").json()

    users_df = pd.DataFrame(users)
    posts_df = pd.DataFrame(posts)
    comments_df = pd.DataFrame(comments)
    todos_df = pd.DataFrame(todos)

    return users_df, posts_df, comments_df, todos_df


def compute_metrics(users_df, posts_df, comments_df, todos_df):
    """Liczy podstawowe metryki na bazie danych z API."""

    # Liczba postów na użytkownika
    posts_per_user = (
        posts_df.groupby("userId")["id"]
        .count()
        .rename("posts_count")
        .reset_index()
    )

    # Liczba komentarzy na post
    comments_per_post = (
        comments_df.groupby("postId")["id"]
        .count()
        .rename("comments_count")
        .reset_index()
    )

    # Średnia liczba komentarzy na post (globalnie)
    avg_comments_per_post = comments_per_post["comments_count"].mean()

    #5 najbardziej komentowanych postów
    top5_commented = comments_per_post.sort_values(
        "comments_count", ascending=False
    ).head(5)
    # tytuły postów
    top5_commented = top5_commented.merge(
        posts_df[["id", "title"]],
        left_on="postId",
        right_on="id",
        how="left"
    ).rename(columns={"title": "post_title"}).drop(columns=["id"])

    # Procent wykonanych TODO per user
    todo_completion = (
        todos_df.groupby("userId")["completed"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "done", "count": "total"})
    )
    todo_completion["completion_pct"] = (
        todo_completion["done"] / todo_completion["total"] * 100
    )

    # nazwy użytkowników
    users_short = users_df[["id", "name", "username"]]
    posts_per_user = posts_per_user.merge(
        users_short,
        left_on="userId",
        right_on="id",
        how="left"
    )
    todo_completion = todo_completion.merge(
        users_short,
        left_on="userId",
        right_on="id",
        how="left"
    )

    return {
        "posts_per_user": posts_per_user,
        "avg_comments_per_post": avg_comments_per_post,
        "top5_commented": top5_commented,
        "todo_completion": todo_completion,
    }


def main():
    st.title("Mini-analityka: JSONPlaceholder API")
    st.caption("Dane z publicznego API: users, posts, comments, todos")

    with st.spinner("Pobieram dane z API..."):
        users_df, posts_df, comments_df, todos_df = fetch_data()

    metrics = compute_metrics(users_df, posts_df, comments_df, todos_df)

    st.header("Podstawowe metryki")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Liczba użytkowników",
            len(users_df)
        )
    with col2:
        st.metric(
            "Średnia liczba komentarzy na post",
            f"{metrics['avg_comments_per_post']:.2f}"
        )

    st.divider()

    st.subheader("Liczba postów na użytkownika")
    posts_chart_df = metrics["posts_per_user"].copy()
    posts_chart_df["label"] = posts_chart_df["username"]
    st.bar_chart(
        data=posts_chart_df,
        x="label",
        y="posts_count",
    )

    st.subheader("Procent wykonanych TODO na użytkownika")
    todo_chart_df = metrics["todo_completion"].copy()
    todo_chart_df["label"] = todo_chart_df["username"]
    st.bar_chart(
        data=todo_chart_df,
        x="label",
        y="completion_pct",
    )

    st.subheader("Top 5 najbardziej komentowanych postów")
    top5 = metrics["top5_commented"].copy()
    # Skrócone tytuły do czytelnej długości na wykresie
    top5["short_title"] = top5["post_title"].str.slice(0, 30) + "..."
    st.bar_chart(
        data=top5,
        x="short_title",
        y="comments_count",
    )

    with st.expander("Podgląd surowych danych"):
        st.write("Users", users_df.head())
        st.write("Posts", posts_df.head())
        st.write("Comments", comments_df.head())
        st.write("Todos", todos_df.head())


if __name__ == "__main__":
    main()
