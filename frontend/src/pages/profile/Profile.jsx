import NavBar from "../../components/global/NavBar";
import SimplifiedPost from "../../components/home/SimplifiedPost";

export default function Profile({ scrollContainerRef, searchTerm, userId }) {
  return (
    <>
      <div>
        raihah insert profile details edit profile over here make it half the
        screen width and height, the user posts i give to you already
      </div>
      <SimplifiedPost
        scrollContainerRef={scrollContainerRef}
        searchTerm={searchTerm}
        userId={userId}
      />
    </>
  );
}
