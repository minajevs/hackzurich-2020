const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const readFiles = (dirname, onFileContent, onError) => {
  fs.readdir(dirname, function (err, filenames) {
    if (err) {
      return;
    }
    filenames.forEach(function (filename) {
      fs.readFile(dirname + `/${filename}`, function (err, content) {
        if (err) {
          return;
        }
        onFileContent(filename, content);
      });
    });
  });
};

const shakalize = async (file, compressRate) => {
  sharp(path.resolve(`./to_shakal/${file}`))
    .blur(++compressRate)
    .grayscale()
    .toFile(path.resolve("./shakalized", `${val}_${name}`), function (
      err,
      info
    ) {
      console.log(err, info);
    });
};

readFiles(path.resolve("./to_shakal"), (name, content) => {
  const sizes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
  sizes.forEach((val) => shakalize(name, val));
});
