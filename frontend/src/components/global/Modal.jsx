export default function Modal({ modal }) {
  return (
    <div className="flex justify-center items-center w-full">
      <section
        className={`absolute w-11/12 md:w-11/12 top-5 text-center z-10 flex justify-center rounded-md tracking-wide opacity-80 font-semibold text-red-700 text-lg ${
          modal.type === "fail" ? "bg-red-200" : "bg-green-400"
        }`}
      >
        {modal.message}
      </section>
    </div>
  );
}
