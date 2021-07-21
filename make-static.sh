rm -rf static
mkdir static

echo "Building Docs....."
cd docs
sphinx-apidoc -o source ..
make html
cd ..

echo "Copying Docs....."
mkdir static/docs
cp -r docs/build/html/ static/docs/

echo "Building App....."
cd web-validator
rm -rf dist/
npm run build
cd ..

echo "Copying App....."
mkdir static/app
cp -r web-validator/dist/ static/app/

echo ".....Done....."