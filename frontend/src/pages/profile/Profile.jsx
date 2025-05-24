import SimplifiedPost from "../../components/home/SimplifiedPost";
import { useContext, useEffect } from "react";
import { GlobalContext } from "../../utils/globalContext";

export default function Profile({ scrollContainerRef, searchTerm }) {
  const { auth } = useContext(GlobalContext);

  useEffect(() => {
    console.log(auth);
  });
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
        userId={auth.user.user_id}
      />
    </>
  );
}
