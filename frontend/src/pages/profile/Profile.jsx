import SimplifiedPost from "../../components/home/SimplifiedPost";

export default function Profile({ scrollContainerRef, searchTerm, userId }) {
  return (
    <>
      <div className="mt-60">
        raihah insert profile details edit profile over here make it half the
        screen height, the user posts i give to you already, need fix the width
        of the posts below also
      </div>
      <SimplifiedPost
        scrollContainerRef={scrollContainerRef}
        searchTerm={searchTerm}
        userId={userId}
      />
    </>
  );
}
